from django.urls import path
from . import views

urlpatterns = [
    path('api/usuarios/', views.listar_usuarios),
    path('api/usuarios/criar/', views.criar_usuario),
    path('usuarios/', views.listar_template),
]