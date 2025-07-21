from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control form-control-md",
            "placeholder": "email@exemplo.com"
        })
    )
    password = forms.CharField(
        label="Senha",
        required=True,
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-md",
            "placeholder": "Sua senha",
            "id": "id_password"
        })
    )
    remember_me = forms.BooleanField(
        label="Lembre-se de mim",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
