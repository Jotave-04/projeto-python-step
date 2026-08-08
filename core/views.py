import bcrypt
import jwt
from datetime import timedelta, datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from core.models import Usuario, Evento, Inscricao
from core.serializers import (
    UsuarioRegistrarSerializer,
    UsuarioLoginSerializer,
    EventoSerializer,
    InscricaoSerializer,
)


# ---------- Autenticação ----------

@api_view(["POST"])
def registrar(request):
    serializer = UsuarioRegistrarSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    dados = serializer.validated_data

    if Usuario.objects.filter(email=dados["email"]).exists():
        return Response({"erro": "Email já cadastrado"}, status=400)

    senha_hash = bcrypt.hashpw(dados["senha"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    usuario = Usuario.objects.create(
        nome=dados["nome"], email=dados["email"], senha=senha_hash, role=dados.get("role", "user"),
    )

    token = jwt.encode(
        {"id": usuario.id, "email": usuario.email, "role": usuario.role, "exp": datetime.utcnow() + timedelta(days=7)},
        settings.SECRET_KEY, algorithm="HS256",
    )

    return Response({
        "mensagem": "Usuário registrado com sucesso",
        "token": token,
        "usuario": {"id": usuario.id, "nome": usuario.nome, "email": usuario.email, "role": usuario.role},
    }, status=201)


@api_view(["POST"])
def login(request):
    serializer = UsuarioLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    dados = serializer.validated_data

    try:
        usuario = Usuario.objects.get(email=dados["email"])
    except Usuario.DoesNotExist:
        return Response({"erro": "Email ou senha inválidos"}, status=401)

    if not bcrypt.checkpw(dados["senha"].encode("utf-8"), usuario.senha.encode("utf-8")):
        return Response({"erro": "Email ou senha inválidos"}, status=401)

    token = jwt.encode(
        {"id": usuario.id, "email": usuario.email, "role": usuario.role, "exp": datetime.utcnow() + timedelta(days=7)},
        settings.SECRET_KEY, algorithm="HS256",
    )

    return Response({
        "mensagem": "Login realizado com sucesso",
        "token": token,
        "usuario": {"id": usuario.id, "nome": usuario.nome, "email": usuario.email, "role": usuario.role},
    })


@api_view(["GET"])
def perfil(request):
    usuario = _usuario_autenticado(request)
    if isinstance(usuario, Response):
        return usuario

    return Response({
        "usuario": {"id": usuario.id, "nome": usuario.nome, "email": usuario.email, "role": usuario.role},
    })


# ---------- Auxiliares de autenticação (usados também pelas views de evento) ----------

def _usuario_autenticado(request):
    """Lê o token JWT do header, valida e retorna o Usuario. Retorna Response de erro se falhar."""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return Response({"erro": "Token não informado"}, status=401)

    try:
        token = auth.split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return Response({"erro": "Token expirado"}, status=401)
    except jwt.InvalidTokenError:
        return Response({"erro": "Token inválido"}, status=401)

    try:
        return Usuario.objects.get(id=payload["id"])
    except Usuario.DoesNotExist:
        return Response({"erro": "Usuário não encontrado"}, status=404)


# ---------- Eventos ----------

@api_view(["GET", "POST"])
def eventos(request):
    if request.method == "GET":
        lista = Evento.objects.all()
        serializer = EventoSerializer(lista, many=True)
        return Response(serializer.data)

    # POST — só admin pode criar
    usuario = _usuario_autenticado(request)
    if isinstance(usuario, Response):
        return usuario

    if usuario.role != "admin":
        return Response({"erro": "Acesso restrito a administradores"}, status=403)

    serializer = EventoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    evento = serializer.save(criado_por=usuario)

    return Response(EventoSerializer(evento).data, status=201)


@api_view(["GET", "PUT", "DELETE"])
def evento_detalhe(request, evento_id):
    try:
        evento = Evento.objects.get(id=evento_id)
    except Evento.DoesNotExist:
        return Response({"erro": "Evento não encontrado"}, status=404)

    if request.method == "GET":
        return Response(EventoSerializer(evento).data)

    # PUT e DELETE — só admin
    usuario = _usuario_autenticado(request)
    if isinstance(usuario, Response):
        return usuario

    if usuario.role != "admin":
        return Response({"erro": "Acesso restrito a administradores"}, status=403)

    if request.method == "PUT":
        serializer = EventoSerializer(evento, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    if request.method == "DELETE":
        evento.delete()
        return Response(status=204)


# ---------- Inscrições ----------

@api_view(["GET", "POST"])
def inscricoes(request, evento_id):
    try:
        evento = Evento.objects.get(id=evento_id)
    except Evento.DoesNotExist:
        return Response({"erro": "Evento não encontrado"}, status=404)

    if request.method == "GET":
        lista = evento.inscricoes.all()
        serializer = InscricaoSerializer(lista, many=True)
        return Response(serializer.data)

    # POST — qualquer usuário autenticado pode se inscrever
    usuario = _usuario_autenticado(request)
    if isinstance(usuario, Response):
        return usuario

    serializer = InscricaoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    inscricao = serializer.save(evento=evento)

    return Response(InscricaoSerializer(inscricao).data, status=201)