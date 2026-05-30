from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Produto

def fazer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        usuario = authenticate(request, username=username, password=senha)

        if usuario is not None:
            login(request, usuario)
            return redirect('pagina_inicial')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'loja/login.html')

@login_required
def pagina_inicial(request):
    produtos = Produto.objects.filter(ativo=True).order_by('nome')
    return render(request, 'loja/inicial.html', {'produtos': produtos})

def fazer_logout(request):
    logout(request)
    return redirect('login')
          