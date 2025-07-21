from datetime import date
from decimal import Decimal

from django.urls import reverse

from src.sales.models import Sale, SaleItem
from src.sales.tests.views.base import BaseSalesTestCase


class ManagementViewsTest(BaseSalesTestCase):
    def setUp(self):
        super().setUp()
        self.sale = Sale.objects.create(
            buyer=self.user,
            cep="123", street="R1", neighborhood="B1", city="Ct1", state="St1",
            total_price=self.prod2.price
        )
        SaleItem.objects.create(
            sale=self.sale, product=self.prod2, quantity=1, unit_price=self.prod2.price
        )

    def test_sales_list_view(self):
        url = reverse("sales:sales_list")
        resp = self.client.get(url)

        self.assertIn(self.sale, resp.context['sales'])
        self.assertEqual(resp.status_code, 200)

    def test_sale_detail_view(self):
        url = reverse("sales:sale_detail", args=[self.sale.id])
        resp = self.client.get(url)
        self.assertContains(resp, f"#{self.sale.id}")

    def test_sale_edit_view_sets_session_and_redirects(self):
        url = reverse("sales:sale_edit", args=[self.sale.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.client.session["sale_id"], self.sale.id)

    def test_update_sale_view_without_edit_id(self):
        session = self.client.session
        session.pop("sale_id", None)
        session.save()

        url = reverse("sales:update_sale", args=[self.sale.id])
        resp = self.client.post(url)

        self.assertEqual(resp.status_code, 302)

        location = resp.headers.get("Location") or resp["Location"]
        expected_url_part = reverse("sales:sale_step_1_products")
        self.assertTrue(
            location.endswith(expected_url_part),
            f"Esperava redirect para {expected_url_part}, mas foi {location}"
        )

    def test_update_sale_view_success(self):
        session = self.client.session
        session["sale_id"] = self.sale.id
        session["cart"] = {str(self.prod2.id): 2}
        session["address_data"] = {"cep":"000","street":"X","neighborhood":"Y","city":"Z","state":"W"}
        session["sale_date"] = date.today().isoformat()
        session.save()

        url = reverse("sales:update_sale", args=[self.sale.id])
        resp = self.client.post(url)

        self.assertEqual(resp.status_code, 302)
        updated = Sale.objects.get(id=self.sale.id)
        self.assertEqual(updated.total_price, Decimal("15.00"))

    def test_sale_delete_view(self):
        url = reverse("sales:sale_delete", args=[self.sale.id])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Sale.objects.filter(id=self.sale.id).exists())
