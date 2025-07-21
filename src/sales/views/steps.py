from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from src.inventory.models import Product
from src.sales.forms import SaleForm
from src.sales.views.utils import clear_sale_session, get_cart_context


@login_required(login_url="/auth/login/")
def sale_step_1_products_view(request: HttpRequest) -> HttpResponse:

    clear_sale_session(request)

    products = Product.objects.all().order_by("name")
    paginator = Paginator(products, 10)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    cart_ctx = get_cart_context(request)
    context = {
        **cart_ctx,
        "page_obj": page_obj,
        "step_number": 1,
        "step_title": "Produtos",
        "total_steps": 3,
        "prev_url": None,
        "next_url": reverse("sales:sale_step_2_address"),
        "next_label": "Próximo: Endereço",
        "edit_sale":     "sale_id" in request.session,
        "sale_id":  request.session.get("sale_id"),
    }
    return render(request, "sales/steps/sale_step_1_products.html", context)



@login_required(login_url="/auth/login/")
def sale_step_2_address_view(request: HttpRequest) -> HttpResponse:
    cart_ctx = get_cart_context(request)
    if not cart_ctx["cart_items"]:
        return redirect("sales:sale_step_1_products")

    if request.method == "POST":
        form = SaleForm(request.POST)
        if form.is_valid():
            request.session["address_data"] = form.cleaned_data
            return redirect("sales:sale_step_3_summary")
    else:
        form = SaleForm(initial=request.session.get("address_data"))

    context = {
        **cart_ctx,
        "form": form,
        "step_number": 2,
        "step_title": "Endereço",
        "total_steps": 3,
        "prev_url": reverse("sales:sale_step_1_products"),
        'next_url':      reverse('sales:sale_step_3_summary'),
        "next_label": "Próximo: Resumo Final",
        'edit_sale':     'sale_id' in request.session,
        'sale_id':  request.session.get('sale_id'),
    }
    return render(request, "sales/steps/sale_step_2_address.html", context)



@login_required(login_url='/auth/login/')
def sale_step_3_summary_view(request: HttpRequest) -> HttpResponse:

    cart_ctx = get_cart_context(request)
    address_data = request.session.get('address_data')

    if not cart_ctx['cart_items'] or not address_data:
        messages.error(request, "Dados da venda incompletos. Por favor, comece novamente.")
        return redirect('sales:sale_step_1_products')

    request.session['subtotal'] = str(cart_ctx['subtotal'])

    if request.method == "POST" and "sale_date" in request.POST:
        raw_date = request.POST["sale_date"]
        try:
            sale_date = date.fromisoformat(raw_date)
        except (ValueError, TypeError):
            sale_date = date.today()
        request.session["sale_date"] = sale_date.isoformat()

    raw = request.session.get("sale_date")
    if raw:
        try:
            sale_date = date.fromisoformat(raw)
        except (ValueError, TypeError):
            sale_date = date.today()
    else:
        sale_date = date.today()
        request.session["sale_date"] = sale_date.isoformat()

    context = {
        **cart_ctx,
        'address_data': address_data,
        'sale_date': sale_date,
        'step_number':  3,
        'step_title':   'Resumo',
        'total_steps':  3,
        'prev_url':     reverse('sales:sale_step_2_address'),
        'submit_label': 'Finalizar Venda',
        'edit_sale':     'sale_id' in request.session,
        'sale_id':  request.session.get('sale_id'),
    }
    return render(request, 'sales/steps/sale_step_3_summary.html', context)


@require_POST
@login_required(login_url="/auth/login/")
def update_sale_date_session(request: HttpRequest) -> HttpResponse:
    raw_date = request.POST.get("sale_date")
    try:
        date.fromisoformat(str(raw_date))
        request.session["sale_date"] = raw_date
        request.session.modified = True
        return HttpResponse(status=204)
    except ValueError:
        return HttpResponse(status=400)
