from django.urls import reverse

from src.sales.tests.views.base import BaseSalesTestCase


class StepViewsTest(BaseSalesTestCase):
    def test_step_1_products_clears_session(self):
        """
        Verifica se ao acessar o passo 1, a sessão de venda é limpa.
        """
        session = self.client.session
        session["cart"] = {"dummy": 1}
        session["sale_id"] = 42
        session.save()

        url = reverse("sales:sale_step_1_products")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertNotIn("sale_id", self.client.session)

    def test_step_2_requires_cart_items(self):
        """
        Verifica se o passo 2 redireciona para o passo 1 se o carrinho estiver vazio.
        """
        url = reverse("sales:sale_step_2_address")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)

        location = resp.headers.get("Location") or resp["Location"]
        expected = reverse("sales:sale_step_1_products")
        self.assertTrue(
            location.endswith(expected),
            f"Esperava redirect para {expected}, mas foi {location}"
        )

    def test_steps_flow_full(self):
        """
        Verifica se os passos 2 e 3 carregam corretamente quando a sessão está preenchida.
        """
        session = self.client.session
        session["cart"] = {str(self.prod1.id): 2}
        session["address_data"] = {"cep":"123","street":"X","neighborhood":"Y","city":"C","state":"S"}
        session.save()

        urls = [
            reverse("sales:sale_step_2_address"),
            reverse("sales:sale_step_3_summary"),
        ]
        for u in urls:
            with self.subTest(url=u):
                resp = self.client.get(u)
                self.assertEqual(resp.status_code, 200, f"Falha ao carregar a URL: {u}")
