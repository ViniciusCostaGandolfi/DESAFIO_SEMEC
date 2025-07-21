class CepServiceError(Exception):
    """Classe base para erros relacionados ao serviço de CEP."""
    pass

class InvalidCepError(CepServiceError):
    """Lançada quando o formato do CEP é inválido."""
    pass

class CepNotFoundError(CepServiceError):
    """Lançada quando o CEP não é encontrado na API ou há um erro de comunicação."""
    pass
