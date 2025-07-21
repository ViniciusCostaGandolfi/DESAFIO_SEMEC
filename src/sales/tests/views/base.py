from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from src.inventory.models import Product


class BaseSalesTestCase(TestCase):
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user( # type: ignore
            email="tester@example.com",
            password="secret",
            full_name="Test User"
        )

        self.client = Client()
        self.client.login(email="tester@example.com", password="secret")

        self.prod1 = Product.objects.create(name="Prod A", price=Decimal("5.00"))
        self.prod2 = Product.objects.create(name="Prod B", price=Decimal("7.50"))
