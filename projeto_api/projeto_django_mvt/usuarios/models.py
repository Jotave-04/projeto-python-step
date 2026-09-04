from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    idade = models.IntegerField(null=True, blank=True)
    data_cadastro = models.DateTimeField(default=timezone.now)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome