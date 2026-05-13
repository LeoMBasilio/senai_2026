"""
filters.py — Define os filtros disponíveis para a listagem de Produtos.

O DjangoFilterBackend usa este arquivo para saber quais query params
a URL aceita e como eles se traduzem em cláusulas WHERE no SQL.

Sem este arquivo, a única filtragem possível seria por campo exato
(?categoria=1). Com ele, temos filtros customizados muito mais flexíveis.

Exemplo de URL com filtros combinados:
  /api/produtos/?preco_min=10&preco_max=50&nome=cafe&ativo=true&categoria__nome=bebidas
"""

import django_filters
from .models import Produto


class ProdutoFilter(django_filters.FilterSet):
    """
    FilterSet = conjunto de filtros para o model Produto.
    Cada atributo aqui vira um query param aceito na URL.
    """

    # NumberFilter com lookup_expr='gte' = "greater than or equal" (>=)
    # ?preco_min=10 → WHERE preco >= 10
    preco_min = django_filters.NumberFilter(field_name='preco', lookup_expr='gte')

    # lookup_expr='lte' = "less than or equal" (<=)
    # ?preco_max=50 → WHERE preco <= 50
    preco_max = django_filters.NumberFilter(field_name='preco', lookup_expr='lte')

    # CharFilter com icontains = busca case-insensitive que contém o valor
    # ?nome=cafe → WHERE nome ILIKE '%cafe%'
    # Sem icontains seria busca exata: WHERE nome = 'cafe' (menos útil)
    nome = django_filters.CharFilter(field_name='nome', lookup_expr='icontains')

    # Filtros por atributos do relacionamento (traversal de FK).
    # Django permite acessar campos de tabelas relacionadas com __ (double underscore).
    # field_name='categoria__nome' = JOIN com tabela Categoria, filtra pelo campo 'nome'
    # ?categoria__nome=bebidas → WHERE categoria.nome ILIKE '%bebidas%'
    categoria__nome = django_filters.CharFilter(
        field_name='categoria__nome',
        lookup_expr='icontains'
    )

    # BooleanFilter aceita: true/false/1/0
    # ?categoria__ativa=true → WHERE categoria.ativa = TRUE
    # Útil para esconder produtos de categorias desativadas
    categoria__ativa = django_filters.BooleanFilter(field_name='categoria__ativa')

    class Meta:
        model = Produto
        # Campos listados aqui usam filtragem EXATA (sem lookup_expr customizado).
        # ?ativo=true → WHERE ativo = TRUE  (exato, não precisa de customização)
        # ?categoria=1 → WHERE categoria_id = 1  (exato por ID)
        # Os campos declarados acima (preco_min, etc.) sobrescrevem qualquer
        # comportamento padrão — por isso não precisam estar aqui também.
        fields = ['ativo', 'categoria', 'preco_min', 'preco_max', 'nome']
