from django.contrib import admin

from .models import Product, ProductSupplier, Supplier


class ProductSupplierInline(admin.TabularInline):
    model = ProductSupplier
    extra = 1


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    inlines = [ProductSupplierInline]


@admin.register(ProductSupplier)
class ProductSupplierAdmin(admin.ModelAdmin):
    list_display = ('product', 'supplier')
    list_select_related = ('product', 'supplier')
    autocomplete_fields = ('product', 'supplier')
