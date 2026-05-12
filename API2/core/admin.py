# admin.py — Registra os models no painel administrativo do Django.
# Acesse /admin/ com o superusuário para gerenciar dados pelo navegador.

from django.contrib import admin
from .models import Categoria, Produto


# O decorator @admin.register(Model) é o atalho moderno para registrar um
# ModelAdmin. É equivalente a escrever admin.site.register(Categoria, CategoriaAdmin).
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    # list_display define quais colunas aparecem na tabela de listagem do admin.
    # Por padrão só aparece o __str__ do objeto; aqui customizamos para mostrar mais.
    list_display = ['id', 'nome', 'ativa']

    # search_fields adiciona uma caixa de busca no topo da listagem.
    # O admin vai buscar pelo campo 'nome' quando o usuário digitar algo.
    search_fields = ['nome']


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Mostra colunas mais úteis na listagem de produtos.
    list_display = ['nome', 'preco', 'estoque', 'ativo', 'categoria']
    search_fields = ['nome']

    # list_filter adiciona filtros na barra lateral direita do admin.
    # Permite clicar para filtrar rapidamente por ativo=True/False ou por categoria.
    list_filter = ['ativo', 'categoria']
