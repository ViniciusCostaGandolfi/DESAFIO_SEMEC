
from abc import ABC, abstractmethod
from typing import Optional

from src.common.address.models import Address


class CepServiceUseCase(ABC):
    """
    Interface para um serviço que busca endereços por CEP.
    """
    @abstractmethod
    async def get_address_by_cep(self, cep: str) -> Optional[Address]:
        """Busca um endereço e retorna a entidade Address ou None se não encontrado."""
        raise NotImplementedError()
