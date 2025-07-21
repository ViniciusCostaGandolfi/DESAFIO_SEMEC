from pydantic import BaseModel, Field, field_validator


class Address(BaseModel):
    """
    Entidade de domínio que representa um endereço, usando Pydantic para validação.
    """
    cep: str
    street: str = Field(alias='logradouro')
    neighborhood: str = Field(alias='bairro')
    city: str = Field(alias='localidade')
    state: str = Field(alias='uf')

    @field_validator('cep', check_fields=False)
    def format_cep(cls, v: str) -> str:
        """Garante que o CEP esteja sempre no formato com hífen."""
        cleaned_cep = "".join(filter(str.isdigit, v))
        if len(cleaned_cep) == 8:
            return f"{cleaned_cep[:5]}-{cleaned_cep[5:]}"
        return v
