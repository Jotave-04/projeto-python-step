# loja/views.py
from django.shortcuts import (
    render, redirect, get_object_or_404
)
from django.contrib.auth.decorators import login_required
from .models import Produto
from .forms import ProdutoForm

@login_required
def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(
        request,
        'loja/lista_produtos.html',
        {'produtos': produtos}
    )

@login_required
def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm()
    return render(
        request,
        'loja/form_produto.html',
        {'form': form, 'titulo': 'Novo Produto'}
    )

@login_required
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(
            request.POST, request.FILES, instance=produto
        )
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(
        request,
        'loja/form_produto.html',
        {
            'form': form,
            'titulo': f'Editar: {produto.nome}',
            'produto': produto
        }
    )

@login_required
def excluir_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('listar_produtos')
    return render(
        request,
        'loja/confirmar_exclusao.html',
        {'produto': produto}
    )