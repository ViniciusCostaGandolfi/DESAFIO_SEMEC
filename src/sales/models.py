from django.db import models
from django.utils import timezone

from config import settings
from src.inventory.models import Product


class Sale(models.Model):
    id = models.BigAutoField(primary_key=True)
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Comprador"
    )
    sale_date = models.DateTimeField(
                default=timezone.now,
                verbose_name="Data da Venda"
    )

    cep = models.CharField(max_length=9, verbose_name="CEP")
    number = models.CharField(max_length=30, verbose_name="Número", default="")
    complement = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    street = models.CharField(max_length=255, verbose_name="Rua / Logradouro")
    neighborhood = models.CharField(max_length=255, verbose_name="Bairro")
    city = models.CharField(max_length=255, verbose_name="Cidade")
    state = models.CharField(max_length=2, verbose_name="Estado (UF)")

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Subtotal da Venda"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Preço Total da Venda"
    )

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
        ordering = ['-sale_date']

    def __str__(self):
        return f"Venda #{self.id} - {self.buyer.username}"

    def get_items(self):
        return SaleItem.objects.filter(sale=self).all()

class SaleItem(models.Model):
    id = models.BigAutoField(primary_key=True)

    sale: models.ForeignKey[Sale] = models.ForeignKey(
        Sale,
        related_name="items",
        on_delete=models.CASCADE,
        verbose_name="Venda"
    )
    product: models.ForeignKey[Product] = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name="Produto"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Quantidade"
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preço Unitário na Venda"
    )

    class Meta:
        verbose_name = "Item da Venda"
        verbose_name_plural = "Itens da Venda"
        unique_together = ['sale', 'product']

    def __str__(self):
        return f"{self.quantity}x {self.product.name} na Venda #{self.sale.id}"

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

