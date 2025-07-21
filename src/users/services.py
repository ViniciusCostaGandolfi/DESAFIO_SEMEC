from typing import Optional, cast

from django.contrib.auth import authenticate, login
from django.forms import Form
from django.http import HttpRequest

from src.users.models import User


class UserService:
    """
    Service layer que opera diretamente com os formulários do Django.
    """
    @staticmethod
    def register_user(form: Form) -> User:
        """
        Cria um novo usuário a partir de um formulário de registro validado.
        """
        email = form.cleaned_data['email']
        full_name = form.cleaned_data['full_name']
        password = form.cleaned_data['password']

        if User.objects.filter(email=email).exists():
            raise ValueError(f"O endereço de e-mail '{email}' já está em uso.")

        user = User.objects.create(
            full_name=full_name,
            email=email,
            password=password
        )
        return user

    @staticmethod
    def authenticate_user(form: Form, request: HttpRequest) -> Optional[User]:
        """
        Verifica as credenciais de um formulário de login validado.
        """
        user = authenticate(
            request,
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        return cast(User, user)

    @staticmethod
    def login_user(request: HttpRequest, user: User) -> None:
        """
        Realiza o login do usuário na sessão.
        """
        login(request, user)
