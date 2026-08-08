from rest_framework import serializers
from core.models import Usuario, Evento, Inscricao


class UsuarioRegistrarSerializer(serializers.Serializer):
    nome = serializers.CharField()
    email = serializers.EmailField()
    senha = serializers.CharField()
    role = serializers.CharField(default="user")


class UsuarioLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField()


class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ["id", "nome", "descricao", "data", "local", "capacidade", "valor", "status", "criado_por"]
        read_only_fields = ["criado_por"]


class InscricaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscricao
        fields = ["id", "nome", "email", "telefone", "evento", "criado_em"]
        read_only_fields = ["evento", "criado_em"]