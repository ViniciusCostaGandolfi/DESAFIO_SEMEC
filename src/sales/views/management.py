from datetime import date
from decimal import Decimal
from typing import cast

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from src.inventory.models import Product
from src.sales.models import Sale, SaleItem
from src.sales.sale_service import get_sale_service
from src.sales.views.utils import clear_sale_session


@login_required(login_url="/auth/login/")
def sale_detail_view(request: HttpRequest, sale_id: int):
    sale = get_object_or_404(Sale, id=sale_id, buyer=request.user)
    return render(request, "sales/sale_detail.html", {"sale": sale})


@login_required(login_url="/auth/login/")
def sale_edit_view(request: HttpRequest, sale_id: int) -> HttpResponse:
    sale = get_object_or_404(Sale, id=sale_id, buyer=request.user)

    clear_sale_session(request)

    request.session["sale_id"] = sale.id

    cart = {str(item.product.id): item.quantity for item in sale.get_items()}
    request.session["cart"] = cart

    request.session["address_data"] = {
        "cep": sale.cep,
        "street": sale.street,
        "neighborhood": sale.neighborhood,
        "city": sale.city,
        "state": sale.state,
        "number": sale.number,
        "complement": sale.complement,
    }

    request.session["sale_date"] = sale.sale_date.isoformat()

    return redirect("sales:sale_step_1_products")


@require_POST
@login_required(login_url="/auth/login/")
def create_sale_view(request: HttpRequest) -> HttpResponse:
    cart = request.session.get("cart")
    address_data = request.session.get("address_data")
    subtotal = request.session.get("subtotal")
    raw_sale_date = request.session.get("sale_date")
    if not cart or not address_data or subtotal is None:
        messages.error(request, "Sua sessão expirou ou os dados estão incompletos.")
        return redirect("sales:sale_step_1_products")
    sale_date = date.fromisoformat(raw_sale_date) if raw_sale_date else date.today()

    sale = Sale(
        buyer=request.user,
        total_price=Decimal(cast(str, subtotal)),
        sale_date=sale_date,
        **address_data
    )
    sale.save()

    products_in_cart = Product.objects.filter(id__in=cart.keys())
    product_map = {str(p.id): p for p in products_in_cart}

    sale_items_to_create = [
        SaleItem(
            sale=sale,
            product=product_map.get(product_id),
            quantity=quantity,
            unit_price=product_map.get(product_id).price, # type: ignore
        )
        for product_id, quantity in cart.items()
        if product_map.get(product_id)
    ]
    SaleItem.objects.bulk_create(sale_items_to_create)

    clear_sale_session(request)

    messages.success(request, "Sua venda foi registrada com sucesso!", extra_tags="show-success-modal")
    return redirect("sales:sales_list")


@require_POST
@login_required(login_url="/auth/login/")
def update_sale_view(request: HttpRequest, sale_id: int) -> HttpResponse:
    """
    Atualiza uma venda existente usando o SaleService para a lógica de negócio.
    """
    cart = request.session.get("cart")
    address_data = request.session.get("address_data")
    raw_sale_date = request.session.get("sale_date")

    if not all([cart, address_data, raw_sale_date]):
        messages.error(request, "Sua sessão expirou ou os dados estão incompletos.")
        return redirect("sales:sale_step_1_products")

    try:
        sale = get_sale_service().update_sale(
            sale_id=sale_id,
            user=request.user,
            cart=cart,
            address_data=address_data,
            raw_date=raw_sale_date
        )

        clear_sale_session(request)

        messages.success(
            request,
            f"Venda #{sale.id} atualizada com sucesso!",
            extra_tags="show-update-modal"
        )
        return redirect("sales:sale_detail", sale_id=sale.id)

    except ValueError as e:
        messages.error(request, str(e))
        return redirect("sales:sale_step_1_products")


@login_required(login_url="/login/")
def sales_list_view(request: HttpRequest) -> HttpResponse:
    sales_queryset = Sale.objects.filter(buyer=request.user).order_by("-sale_date")
    paginator = Paginator(sales_queryset, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"sales": page_obj}
    return render(request, "sales/sales_list.html", context)


@require_POST
@login_required(login_url="/auth/login/")
def sale_delete_view(request: HttpRequest, sale_id: int) -> HttpResponse:
    sale = get_object_or_404(Sale, id=sale_id, buyer=request.user)
    sale.delete()
    messages.success(request, f"Venda #{sale_id} excluída com sucesso!", extra_tags="show-delete-modal")
    return redirect("sales:sales_list")
