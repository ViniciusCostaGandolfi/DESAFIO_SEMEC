from datetime import date
from decimal import Decimal

from django.urls import reverse

from src.sales.models import Sale, SaleItem
from src.sales.tests.views.base import BaseSalesTestCase


class CheckoutViewsTest(BaseSalesTestCase):
    def test_create_sale_without_cart(self):
        url = reverse("sales:create_sale")
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.headers["Location"].endswith(reverse("sales:sale_step_1_products")))

    def test_create_sale_success(self):
        session = self.client.session

        session["cart"] = {str(self.prod1.id): 3}

        session["address_data"] = {
            "cep": "123",
            "street": "R",
            "neighborhood": "B",
            "city": "Ct",
            "state": "St"
        }


        session["subtotal"] = str(Decimal("15.00"))
        session["sale_date"] = date.today().isoformat()

        session.save()

        url = reverse("sales:create_sale")
        resp = self.client.post(url)

        self.assertEqual(resp.status_code, 302, "A view deveria redirecionar após o sucesso.")

        sale = Sale.objects.get(buyer=self.user)

        self.assertEqual(sale.total_price, Decimal("15.00"))

        items = SaleItem.objects.filter(sale=sale)
        self.assertEqual(items.count(), 1, "Deveria haver um item na venda.")

        item = items.first()
        self.assertEqual(item.product, self.prod1) # type: ignore
        self.assertEqual(item.quantity, 3) # type: ignore
