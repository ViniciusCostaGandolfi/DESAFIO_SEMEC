from django.db import models


class Supplier(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
        verbose_name="Nome do Fornecedor"
    )

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
        verbose_name="Nome do Produto"
    )
    description = models.CharField(max_length=512, verbose_name="Descrição do Produto", null=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preço de Venda"
    )
    suppliers = models.ManyToManyField(
        Supplier,
        through='ProductSupplier',
        related_name='products',
        verbose_name="Fornecedores"
    )

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return f"{self.name} - R$ {self.price}"

class ProductSupplier(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Produto"
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        verbose_name="Fornecedor"
    )

    class Meta:
        verbose_name = "Fornecedor do Produto"
        verbose_name_plural = "Fornecedores do Produto"
        unique_together = ['product', 'supplier']

    def __str__(self):
        return f"{self.product.name} fornecido por {self.supplier.name}"
