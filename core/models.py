from django.db import models


class Usuario(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=200)
    role = models.CharField(max_length=10, default="user")


class Evento(models.Model):
    STATUS_CHOICES = [
        ("planejado", "Planejado"),
        ("confirmado", "Confirmado"),
        ("realizado", "Realizado"),
        ("cancelado", "Cancelado"),
    ]

    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    data = models.DateTimeField()
    local = models.CharField(max_length=200)
    capacidade = models.IntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="planejado")
    criado_por = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="eventos")


class Inscricao(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="inscricoes")
    criado_em = models.DateTimeField(auto_now_add=True)