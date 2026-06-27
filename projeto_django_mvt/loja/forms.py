# loja/forms.py
from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome', 'preco', 'descricao',
            'estoque', 'imagem', 'ativo'
        ]
        widgets = {
            'descricao': forms.Textarea(
                attrs={'rows': 4}
            ),
            'preco': forms.NumberInput(
                attrs={'step': '0.01', 'min': '0'}
            ),
        }