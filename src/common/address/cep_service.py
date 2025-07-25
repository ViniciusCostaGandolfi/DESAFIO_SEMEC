

import re
from typing import Optional

import httpx

from config import settings
from src.common.address.cep_use_case import CepServiceUseCase
from src.common.address.models import Address

from .exceptions import CepNotFoundError


class AddressFromCep(CepServiceUseCase):

    async def get_address_by_cep(self, cep: str) -> Optional[Address]:

        cep_pattern = r'^\d{5}-?\d{3}$'

        if not re.match(cep_pattern, cep):
            return None

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f'{settings.VIA_CEP_URL}/ws/{cep}/json', timeout=5
                )

                response.raise_for_status()

                data = response.json()



                return Address.model_validate(data)

            except httpx.HTTPStatusError as e:
                raise CepNotFoundError(f"Erro ao consultar a API de CEP para {cep}.") from e
            except httpx.RequestError as e:
                raise CepNotFoundError(f"Erro de comunicação ao buscar o CEP {cep}.") from e
