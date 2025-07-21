

from django.urls import reverse

from src.sales.tests.views.base import BaseSalesTestCase


class CartViewsTest(BaseSalesTestCase):
    def test_add_item_view(self):
        url = reverse("sales:add_item", args=[self.prod1.id])
        resp = self.client.post(url, HTTP_HX_REQUEST="true")
        self.assertEqual(resp.status_code, 200)
        session_cart = self.client.session["cart"]
        self.assertEqual(session_cart[str(self.prod1.id)], 1)

    def test_remove_item_view(self):
        session = self.client.session
        session["cart"] = {str(self.prod1.id): 1}
        session.save()

        url = reverse("sales:remove_item", args=[self.prod1.id])
        resp = self.client.post(url, HTTP_HX_REQUEST="true")
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(str(self.prod1.id), self.client.session.get("cart", {}))

    def test_increase_and_decrease_quantity(self):
        session = self.client.session
        session["cart"] = {str(self.prod2.id): 1}
        session.save()

        inc_url = reverse("sales:increase_quantity", args=[self.prod2.id])
        self.client.post(inc_url, HTTP_HX_REQUEST="true")
        self.assertEqual(self.client.session["cart"][str(self.prod2.id)], 2)

        dec_url = reverse("sales:decrease_quantity", args=[self.prod2.id])
        self.client.post(dec_url, HTTP_HX_REQUEST="true")
        self.assertEqual(self.client.session["cart"][str(self.prod2.id)], 1)
