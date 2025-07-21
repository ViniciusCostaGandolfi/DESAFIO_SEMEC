from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms.login_form import LoginForm
from .forms.register_form import RegistrationForm
from .services import UserService


def login_view(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.user.is_authenticated:
        return redirect('sales:sales_list')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = UserService.authenticate_user(form, request=request)

            if user is not None:
                UserService.login_user(request, user)
                messages.success(request, f"Bem-vindo(a), {user.full_name or user.email}!")
                return redirect('sales:sales_list')
            else:
                messages.error(request, "Credenciais inválidas. Verifique seu e-mail e senha.")
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def register_view(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.user.is_authenticated:
        return redirect('sales:sales_list')

    if request.method == "GET":
        form = RegistrationForm()
        return render(request, 'users/register.html', {'form': form})

    form = RegistrationForm(request.POST)
    if form.is_valid():
        try:
            user = UserService.register_user(form)
            UserService.login_user(request, user)
            messages.success(request, "Conta criada com sucesso!")
            return redirect('sales:sales_list')
        except ValueError as e:
            messages.error(request, str(e))
    else:
        messages.error(request, "Corrija os erros abaixo para continuar.")

    return render(request, 'users/register.html', {'form': form})


def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)
    messages.info(request, "Você foi desconectado com sucesso.")
    return redirect('users:login')
