from decimal import Decimal

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from src.inventory.models import Product


def get_cart_context(request: HttpRequest) -> dict:
    """Função auxiliar para obter o contexto do carrinho da sessão."""
    cart = request.session.get("cart", {})
    cart_items = []
    subtotal = Decimal("0.00")
    total_items = 0

    if cart:
        product_ids = cart.keys()
        products_in_cart = Product.objects.filter(id__in=product_ids)
        product_map = {str(p.id): p for p in products_in_cart}

        for pid, qty in cart.items():
            prod = product_map.get(pid)
            if prod:
                item_subtotal = prod.price * qty
                subtotal += item_subtotal
                total_items += qty
                cart_items.append({"product": prod, "quantity": qty, "subtotal": item_subtotal})

    cart_items.sort(key=lambda item: item["product"].name)
    return {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "cart_item_count": total_items,
    }


def recalculate_cart_and_get_response(request: HttpRequest, cart: dict) -> HttpResponse:
    """
    Recalcula o subtotal, itens totais e renderiza a resposta HTMX.
    Usa o novo _get_cart_context para evitar duplicação.
    """
    request.session["cart"] = cart
    request.session.modified = True

    context = get_cart_context(request)
    return render(request, "sales/partials/htmx_response.html", context)


def clear_sale_session(request: HttpRequest):
    """Limpa os dados da venda da sessão após a conclusão."""
    if "cart" in request.session:
        del request.session["cart"]
    if "address_data" in request.session:
        del request.session["address_data"]
    if "sale_id" in request.session:
        del request.session["sale_id"]
    if "sale_date" in request.session:
        del request.session["sale_date"]

