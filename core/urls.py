from django.urls import path
from core.views import registrar, login, perfil, eventos, evento_detalhe, inscricoes, index

urlpatterns = [
    path("", index, name="index"),

    path("registrar", registrar, name="registrar"),
    path("login", login, name="login"),
    path("me", perfil, name="perfil"),

    path("eventos", eventos, name="eventos"),
    path("eventos/<int:evento_id>", evento_detalhe, name="evento_detalhe"),
    path("eventos/<int:evento_id>/inscricoes", inscricoes, name="inscricoes"),
]