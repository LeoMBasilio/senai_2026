from django.contrib import admin
from .models import Categoria, Produto, Pedido, ItemPedido


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'ativa']
    list_filter = ['ativa']
    search_fields = ['nome']


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'preco', 'estoque', 'ativo', 'categoria', 'criado_em']
    list_filter = ['ativo', 'categoria']
    search_fields = ['nome', 'descricao', 'tags']
    ordering = ['-criado_em']


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'status', 'criado_em']
    list_filter = ['status']
    inlines = [ItemPedidoInline]
