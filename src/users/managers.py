from typing import TYPE_CHECKING

from django.contrib.auth.models import BaseUserManager

if TYPE_CHECKING:
    from .models import User


class UserManager(BaseUserManager["User"]):
    """
    Manager customizado para o modelo User, onde o email é o identificador único
    para autenticação em vez do username.
    """
    def _create_user(self, email: str, full_name: str, password: str | None, **extra_fields) -> "User":
        """
        Método privado que cria e salva um usuário com os dados e campos extras fornecidos.
        Centraliza a lógica de criação.
        """
        if not email:
            raise ValueError("O campo Email é obrigatório")
        if not full_name:
            raise ValueError("O campo Nome Completo é obrigatório")

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, full_name: str, password: str | None = None, **extra_fields) -> "User":
        """
        Cria e salva um usuário padrão com o email, nome completo e senha.
        Garante que um usuário padrão nunca seja staff ou superusuário.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, full_name, password, **extra_fields)

    def create_superuser(self, email: str, full_name: str, password: str | None = None, **extra_fields) -> "User":
        """
        Cria e salva um superusuário com as permissões corretas.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superusuário deve ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusuário deve ter is_superuser=True.")

        return self._create_user(email, full_name, password, **extra_fields)
