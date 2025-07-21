from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from src.inventory.models import Product, Supplier


class ProductSearchHtmxTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        User = get_user_model()
        cls.user = User.objects.create_user( # type: ignore
            email='testuser@example.com',
            password='password123',
            full_name='Test User'
        )
        cls.sup1 = Supplier.objects.create(name='Fornecedor A')
        cls.sup2 = Supplier.objects.create(name='Fornecedor B')

        for i in range(12):
            p = Product.objects.create(name=f'Produto {i}', price=Decimal(10 + i))
            if i % 2 == 0:
                p.suppliers.add(cls.sup1)
            else:
                p.suppliers.add(cls.sup2)

    def setUp(self) -> None:
        self.client.login(email='testuser@example.com', password='password123')

    def test_default_search_loads_successfully(self) -> None:
        url = reverse('inventory:product_search')
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/partials/product_list.html')

    def test_search_by_name_loads_successfully(self) -> None:
        url = reverse('inventory:product_search')
        response = self.client.get(url, {'q': 'Produto 1'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_filter_by_supplier_loads_successfully(self) -> None:
        url = reverse('inventory:product_search')
        response = self.client.get(url, {'supplier': str(self.sup1.id)}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_order_descending_loads_successfully(self) -> None:
        url = reverse('inventory:product_search')
        response = self.client.get(url, {'sort_by': 'name', 'sort_dir': 'desc'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_pagination_next_page_loads_successfully(self) -> None:
        url = reverse('inventory:product_search')
        response = self.client.get(url, {'page': 2}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
