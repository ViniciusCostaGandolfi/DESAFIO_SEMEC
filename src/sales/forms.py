from django import forms

from .models import Sale


class SaleForm(forms.ModelForm):
    """
    Formulário para os dados de endereço de uma nova venda.
    """
    class Meta:
            model = Sale
            fields = ['cep', 'street', 'number', 'complement', 'neighborhood', 'city', 'state']
            widgets = {
                'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o CEP...'}),
                'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua / Logradouro'}),
                'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
                'complement': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apartamento, bloco, etc. (opcional)'}),
                'neighborhood': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
                'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
                'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UF'}),
            }
