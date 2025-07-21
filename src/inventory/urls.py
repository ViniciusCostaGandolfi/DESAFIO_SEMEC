from django.urls import path

from src.inventory.views import product_search_view

urlpatterns = [
    path('products/search/', product_search_view, name='product_search'),
]
