
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from src.inventory.models import Product
from src.sales.views.utils import recalculate_cart_and_get_response


@require_POST
@login_required
def add_item_view(request: HttpRequest, product_id: int) -> HttpResponse:
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {})
    item_id = str(product.id)
    cart[item_id] = cart.get(item_id, 0) + 1
    messages.success(request, f"'{product.name}' foi adicionado à venda.")

    response = recalculate_cart_and_get_response(request, cart)
    response["HX-Trigger"] = "display-message"
    return response


@require_POST
@login_required
def remove_item_view(request: HttpRequest, product_id: int) -> HttpResponse:
    cart = request.session.get("cart", {})
    item_id = str(product_id)
    if item_id in cart:
        del cart[item_id]
        messages.info(request, "Item removido da venda.")
    response = recalculate_cart_and_get_response(request, cart)
    response["HX-Trigger"] = "display-message"
    return response


@require_POST
@login_required
def increase_quantity_view(request: HttpRequest, product_id: int) -> HttpResponse:
    cart = request.session.get("cart", {})
    item_id = str(product_id)
    if item_id in cart:
        cart[item_id] += 1
    return recalculate_cart_and_get_response(request, cart)


@require_POST
@login_required
def decrease_quantity_view(request: HttpRequest, product_id: int) -> HttpResponse:
    cart = request.session.get("cart", {})
    item_id = str(product_id)
    if item_id in cart:
        if cart[item_id] > 1:
            cart[item_id] -= 1
        else:
            del cart[item_id]
            messages.info(request, "Item removido da venda.")
            response = recalculate_cart_and_get_response(request, cart)
            response["HX-Trigger"] = "display-message"
            return response
    return recalculate_cart_and_get_response(request, cart)
