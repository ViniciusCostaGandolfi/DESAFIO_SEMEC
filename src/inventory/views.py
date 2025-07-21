
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from src.inventory.models import Product, Supplier


@login_required
def product_search_view(request: HttpRequest) -> HttpResponse:
    """
    HTMX snippet: busca produtos por nome, filtra por fornecedor
    e ordena, sem filtros de preço.
    """
    q           = request.GET.get('q', '').strip()
    supplier_id = request.GET.get('supplier', '').strip()
    sort_by     = request.GET.get('sort_by', 'name')
    sort_dir    = request.GET.get('sort_dir', 'asc')
    page_number = request.GET.get('page', 1)

    qs = Product.objects.prefetch_related('suppliers').all()
    if q:
        qs = qs.filter(name__icontains=q)
    if supplier_id:
        qs = qs.filter(suppliers__id=supplier_id)

    allowed = {'name': 'name', 'price': 'price'}
    field   = allowed.get(sort_by, 'name')
    if sort_dir == 'desc':
        field = f'-{field}'
    qs = qs.order_by(field).distinct()

    paginator = Paginator(qs, 10)
    page_obj  = paginator.get_page(page_number)

    suppliers = Supplier.objects.order_by('name')

    context = {
        'page_obj':          page_obj,
        'suppliers':         suppliers,
        'current_q':         q,
        'current_supplier':  supplier_id,
        'current_sort_by':   sort_by,
        'current_sort_dir':  sort_dir,
    }
    return render(request, 'inventory/partials/product_list.html', context)
