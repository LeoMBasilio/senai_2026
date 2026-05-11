# ============================================================
# filters.py — Define filtros personalizados para a listagem
#
# Filtros permitem que o cliente da API passe parâmetros na
# URL para buscar apenas os dados que precisa, por exemplo:
#
#   /api/produtos/?ativo=true
#   /api/produtos/?preco_min=50&preco_max=200
#   /api/produtos/?nome=cafe
#
# Sem filtros, a API sempre retornaria TODOS os produtos.
# ============================================================

import django_filters      # biblioteca de filtros para Django REST
from .models import Produto # importa o model que será filtrado


# FilterSet agrupa todos os filtros de um Model em uma só classe.
class ProdutoFilter(django_filters.FilterSet):

    # Filtro de preço mínimo: ?preco_min=50
    # field_name='preco'  → qual coluna do banco usar
    # lookup_expr='gte'   → "greater than or equal" = maior ou igual (>=)
    preco_min = django_filters.NumberFilter(
        field_name='preco', lookup_expr='gte')

    # Filtro de preço máximo: ?preco_max=200
    # lookup_expr='lte' → "less than or equal" = menor ou igual (<=)
    preco_max = django_filters.NumberFilter(
        field_name='preco', lookup_expr='lte')

    # Filtro por nome: ?nome=cafe
    # lookup_expr='icontains' → busca o texto em qualquer parte do nome,
    #                           sem diferenciar maiúsculas de minúsculas
    #                           (ex: "cafe", "Cafe" e "CAFE" retornam igual)
    nome = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Produto
        # Lista quais filtros ficam disponíveis na URL.
        # 'ativo' usa filtro exato automático: ?ativo=true ou ?ativo=false
        fields = ['ativo', 'preco_min', 'preco_max', 'nome']
