from django.contrib import admin

from .models import Sale, SaleItem


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'sale', 'product', 'quantity', 'unit_price', 'subtotal')
    search_fields = ('product__name', 'sale__id')


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    readonly_fields = ('subtotal',)
    extra = 1


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    inlines = [SaleItemInline]

    list_display = ('id', 'buyer', 'sale_date', 'city', 'state', 'total_price')

    list_filter = ('sale_date', 'state')

    search_fields = ('id', 'buyer__username', 'buyer__full_name', 'city')

    readonly_fields = ('total_price', 'subtotal')

    fieldsets = (
        ("Informações Principais", {
            'fields': ('buyer', 'sale_date')
        }),
        ("Endereço de Entrega", {
            'classes': ('collapse',),
            'fields': ('cep', 'street', 'number', 'complement', 'neighborhood', 'city', 'state'),
        }),
        ("Valores", {
            'fields': ('subtotal', 'total_price')
        }),
    )
