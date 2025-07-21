import asyncio

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from src.common.address.cep_service import AddressFromCep
from src.common.address.exceptions import CepNotFoundError, InvalidCepError
from src.sales.forms import SaleForm


@login_required(login_url="/login/")
def check_cep_view(request: HttpRequest) -> HttpResponse:
    cep = request.POST.get("cep")
    if not cep:
        return render(request, "sales/partials/address_fields.html", {"form": SaleForm()})
    service = AddressFromCep()
    try:
        address = asyncio.run(service.get_address_by_cep(cep))
        if not address:
            raise CepNotFoundError(f"O CEP '{cep}' não foi encontrado.")
        address_data = {
            "cep": address.cep,
            "street": address.street,
            "neighborhood": address.neighborhood,
            "city": address.city,
            "state": address.state,
        }
        form = SaleForm(initial=address_data)
    except (InvalidCepError, CepNotFoundError) as e:
        messages.error(request, str(e))
        response = render(request, "shared/messages.html")
        response["HX-Trigger"] = "display-message"
        response.content += render(request, "sales/partials/address_fields.html", {"form": SaleForm()}).content
        return response
    return render(request, "sales/partials/address_fields.html", {"form": form})
