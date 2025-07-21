from unittest.mock import AsyncMock, MagicMock, patch

import httpx
from asgiref.sync import async_to_sync
from django.test import TestCase

from src.common.address.cep_service import AddressFromCep
from src.common.address.exceptions import CepNotFoundError
from src.common.address.models import Address


class AddressModelTest(TestCase):
    def test_format_cep_strips_and_formats(self) -> None:
        data: dict[str, str] = {
            'cep': '12345678',
            'logradouro': 'Rua A',
            'bairro': 'Bairro B',
            'localidade': 'Cidade C',
            'uf': 'SC'
        }
        addr: Address = Address.model_validate(data)
        self.assertEqual(addr.cep, '12345-678')
        self.assertEqual(addr.street, 'Rua A')
        self.assertEqual(addr.neighborhood, 'Bairro B')
        self.assertEqual(addr.city, 'Cidade C')
        self.assertEqual(addr.state, 'SC')

        data['cep'] = '87654-321'
        addr2 = Address.model_validate(data)
        self.assertEqual(addr2.cep, '87654-321')


class AddressFromCepServiceTest(TestCase):
    def setUp(self) -> None:
        self.service: AddressFromCep = AddressFromCep()
        self.valid_cep: str = '12345-678'
        self.raw_data: dict[str, str] = {
            'cep': self.valid_cep,
            'logradouro': 'Rua Teste',
            'bairro': 'Bairro Teste',
            'localidade': 'Cidade Teste',
            'uf': 'TT'
        }

    def test_invalid_cep_format_returns_none(self) -> None:
        result = async_to_sync(self.service.get_address_by_cep)('invalid')
        self.assertIsNone(result)

    @patch('src.common.address.cep_service.httpx.AsyncClient')
    def test_nonexistent_cep_returns_none(self, mock_client_cls: AsyncMock) -> None:
        mock_client = mock_client_cls.return_value.__aenter__.return_value

        mock_response = MagicMock()
        mock_response.json = AsyncMock(return_value={'erro': True})
        mock_client.get.return_value = mock_response

        result = async_to_sync(self.service.get_address_by_cep)(self.valid_cep)
        self.assertIsNone(result)
        mock_client.get.assert_called_once()

    @patch('src.common.address.cep_service.httpx.AsyncClient')
    def test_successful_cep_returns_address(self, mock_client_cls: AsyncMock) -> None:
        mock_client = mock_client_cls.return_value.__aenter__.return_value

        mock_response = MagicMock()
        mock_response.json = AsyncMock(return_value=self.raw_data)

        mock_client.get.return_value = mock_response

        addr = async_to_sync(self.service.get_address_by_cep)(self.valid_cep)
        self.assertIsNotNone(addr)
        self.assertEqual(getattr(addr, 'street', None), 'Rua Teste')
        self.assertEqual(getattr(addr, 'cep', None), self.valid_cep)

    @patch('src.common.address.cep_service.httpx.AsyncClient')
    def test_http_status_error_raises(self, mock_client_cls: AsyncMock) -> None:
        mock_client = mock_client_cls.return_value.__aenter__.return_value
        request = httpx.Request('GET', 'https://example.com')
        response = httpx.Response(404)
        error = httpx.HTTPStatusError('error', request=request, response=response)
        mock_client.get.side_effect = error

        with self.assertRaises(CepNotFoundError):
            async_to_sync(self.service.get_address_by_cep)(self.valid_cep)

    @patch('src.common.address.cep_service.httpx.AsyncClient')
    def test_request_error_raises(self, mock_client_cls: AsyncMock) -> None:
        mock_client = mock_client_cls.return_value.__aenter__.return_value
        err = httpx.RequestError('network error')
        mock_client.get.side_effect = err

        with self.assertRaises(CepNotFoundError):
            async_to_sync(self.service.get_address_by_cep)(self.valid_cep)
