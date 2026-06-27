from rest_framework import serializers
from .models import Tarefa

class TarefaSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.ReadOnlyField(source='usuario.username')

    class Meta:
        model = Tarefa
        fields = [
            'id', 'titulo', 'descricao', 'concluida', 'prioridade',
            'data_criacao', 'data_conclusao', 'usuario', 'usuario_nome'
        ]
        read_only_fields = ['usuario', 'data_criacao', 'data_conclusao']

    def validate_titulo(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("O título deve ter pelo menos 3 caracteres.")
        return value