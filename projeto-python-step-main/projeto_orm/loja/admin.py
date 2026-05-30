from django.contrib import admin
from .models import Categoria, Produto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'preco', 'estoque', 'ativo', 'categoria', 'criado_em')
    list_filter = ('ativo', 'categoria')
    search_fields = ('nome',)
    ordering = ('-criado_em',)
    list_per_page = 15
          