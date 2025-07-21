from django import forms

from src.users.models import User


class RegistrationForm(forms.Form):
    """
    Formulário para validar os dados de registro de um novo usuário.
    Não contém lógica de salvamento no banco de dados.
    """
    full_name = forms.CharField(
        label="Nome Completo",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Endereço de E-mail",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password_confirmation = forms.CharField(
        label="Confirme a Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_email(self):
        """Valida se o email já está em uso."""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este endereço de e-mail já está em uso.")
        return email

    def clean(self):
        """Valida se as senhas coincidem."""
        cleaned_data = super().clean()
        if cleaned_data:
            password = cleaned_data.get("password")
            password_confirmation = cleaned_data.get("password_confirmation")

            if password and password_confirmation and password != password_confirmation:
                self.add_error("password_confirmation", "As senhas não coincidem.")
            return cleaned_data
