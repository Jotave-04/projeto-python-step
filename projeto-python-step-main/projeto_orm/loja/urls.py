from django.urls import path
from . import views

urlpatterns = [
    path('', views.fazer_login, name='login'),
    path('inicial/', views.pagina_inicial, name='pagina_inicial'),
    path('logout/', views.fazer_logout, name='logout'),
]
          