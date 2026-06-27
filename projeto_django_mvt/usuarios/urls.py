from django.urls import path
from . import views

urlpatterns = [
    # Template endpoints
    path('', views.listar_template, name='listar_template'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]