from django.urls import path

from src.sales.views.address import check_cep_view
from src.sales.views.cart import add_item_view, decrease_quantity_view, increase_quantity_view, remove_item_view
from src.sales.views.management import create_sale_view, sale_delete_view, sale_detail_view, sale_edit_view, sales_list_view, update_sale_view
from src.sales.views.steps import (
    sale_step_1_products_view,
    sale_step_2_address_view,
    sale_step_3_summary_view,
    update_sale_date_session,
)

urlpatterns = [
    path('', sales_list_view, name='sales_list'),

    path('<int:sale_id>/', sale_detail_view, name='sale_detail'),
    path('<int:sale_id>/edit/', sale_edit_view, name='sale_edit'),
    path('create/', create_sale_view, name='create_sale'),
    path('<int:sale_id>/update/', update_sale_view, name='update_sale'),
    path('<int:sale_id>/delete/', sale_delete_view, name='sale_delete'),

    path('steps/products/', sale_step_1_products_view, name='sale_step_1_products'),
    path('steps/address/', sale_step_2_address_view, name='sale_step_2_address'),
    path('steps/summary/', sale_step_3_summary_view, name='sale_step_3_summary'),




    path('check-cep/', check_cep_view, name='check_cep'),
    path('add-item/<int:product_id>/', add_item_view, name='add_item'),
    path('increase-item/<int:product_id>/', increase_quantity_view, name='increase_quantity'),
    path('decrease-item/<int:product_id>/', decrease_quantity_view, name='decrease_quantity'),
    path('remove-item/<int:product_id>/', remove_item_view, name='remove_item'),
    path('steps/update-sale-date-session/', update_sale_date_session, name='update_sale_date_session'),



]
