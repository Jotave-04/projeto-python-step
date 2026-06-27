from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer

# View de login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('listar_template')
        else:
            return render(request, 'usuarios/login.html', {'erro': 'Usuário ou senha inválidos'})
    
    return render(request, 'usuarios/login.html')

# View de logout
def logout_view(request):
    logout(request)
    return redirect('login')

# View de registro de novo usuário
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            return render(request, 'usuarios/register.html', {'erro': 'Senhas não coincidem'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'usuarios/register.html', {'erro': 'Email já cadastrado'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'usuarios/register.html', {
                'erro': 'Nome de usuário já existe'
            })
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('listar_template')
    
    return render(request, 'usuarios/register.html')

# Template HTML (protegido)
@login_required(login_url='login')
def listar_template(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})

# ========== FUNÇÃO PARA CRIAR USUÁRIO VIA TEMPLATE ==========

@api_view(['GET', 'POST'])
def criar_usuario_api(request):
    if request.method == 'POST':
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('listar_template')
    return render(request, 'usuarios/register.html')