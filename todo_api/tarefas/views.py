from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Tarefa
from .serializers import TarefaSerializer
from .permissions import EhDono

class TarefaViewSet(viewsets.ModelViewSet):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    permission_classes = [IsAuthenticated, EhDono]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['concluida', 'prioridade']
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['data_criacao', 'prioridade', 'titulo']
    ordering = ['-data_criacao']

    def get_queryset(self):
        # Cada usuário só vê as próprias tarefas
        return Tarefa.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        # Associa a tarefa ao usuário logado automaticamente
        serializer.save(usuario=self.request.user)

    # Ação extra: POST /tarefas/{id}/concluir/
    @action(detail=True, methods=['post'])
    def concluir(self, request, pk=None):
        tarefa = self.get_object()
        if tarefa.concluida:
            return Response(
                {'erro': 'Esta tarefa já está concluída.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        tarefa.concluida = True
        tarefa.data_conclusao = timezone.now()
        tarefa.save()
        return Response({'status': 'tarefa concluída com sucesso'})

    # Ação extra: POST /tarefas/{id}/reabrir/
    @action(detail=True, methods=['post'])
    def reabrir(self, request, pk=None):
        tarefa = self.get_object()
        if not tarefa.concluida:
            return Response(
                {'erro': 'Esta tarefa não está concluída.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        tarefa.concluida = False
        tarefa.data_conclusao = None
        tarefa.save()
        return Response({'status': 'tarefa reaberta com sucesso'})

    # Ação extra: GET /tarefas/estatisticas/
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        tarefas = self.get_queryset()
        total = tarefas.count()
        concluidas = tarefas.filter(concluida=True).count()
        pendentes = total - concluidas

        return Response({
            'total': total,
            'concluidas': concluidas,
            'pendentes': pendentes,
            'porcentagem_concluida': round((concluidas / total * 100) if total > 0 else 0, 1),
        })