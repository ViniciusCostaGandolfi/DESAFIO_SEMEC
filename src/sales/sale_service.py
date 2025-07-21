from datetime import date
from decimal import Decimal

from django.shortcuts import get_object_or_404

from src.inventory.models import Product
from src.sales.models import Sale, SaleItem


class SaleService:
    @staticmethod
    def validate_session_data(session) -> tuple[dict, dict]:
        cart = session.get("cart")
        address_data = session.get("address_data")

        if not cart or not address_data:
            raise ValueError("Dados incompletos ou sessão expirada.")

        return cart, address_data

    @staticmethod
    def create_sale(user, cart, address_data, raw_date: str) -> Sale:
        try:
            sale_date = date.fromisoformat(raw_date)
        except (TypeError, ValueError):
            sale_date = date.today()

        subtotal = SaleService.calculate_subtotal(cart)

        sale = Sale(buyer=user, total_price=subtotal, sale_date=sale_date, **address_data)
        sale.save()

        SaleService.create_sale_items(sale, cart)
        return sale

    @staticmethod
    def update_sale(sale_id, user, cart, address_data, raw_date) -> Sale:
        sale = get_object_or_404(Sale, id=sale_id, buyer=user)

        try:
            sale.sale_date = date.fromisoformat(str(raw_date))
        except (TypeError, ValueError):
            sale.sale_date = date.today()

        sale.cep = address_data["cep"]
        sale.street = address_data["street"]
        sale.neighborhood = address_data["neighborhood"]
        sale.city = address_data["city"]
        sale.state = address_data["state"]
        sale.number = address_data.get("number", "")
        sale.complement = address_data.get("complement", "")

        subtotal = SaleService.calculate_subtotal(cart)
        sale.total_price = subtotal
        sale.save()

        SaleItem.objects.filter(sale=sale).delete()
        SaleService.create_sale_items(sale, cart)

        return sale

    @staticmethod
    def calculate_subtotal(cart: dict) -> Decimal:
        subtotal = Decimal("0.00")
        products = Product.objects.filter(id__in=cart.keys())
        product_map = {str(p.id): p for p in products}

        for prod_id, qty in cart.items():
            product = product_map.get(prod_id)
            if product:
                subtotal += product.price * qty

        return subtotal

    @staticmethod
    def create_sale_items(sale: Sale, cart: dict) -> None:
        products = Product.objects.filter(id__in=cart.keys())
        product_map = {str(p.id): p for p in products}

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

sale_service = SaleService()

def get_sale_service() -> SaleService:
    return sale_service
