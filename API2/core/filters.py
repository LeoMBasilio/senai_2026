# filters.py — Define filtros avançados para a listagem de Produtos.
# O DjangoFilterBackend usa esta classe para transformar query params da URL
# em filtros automáticos no queryset do banco de dados.

import django_filters
from .models import Produto


class ProdutoFilter(django_filters.FilterSet):
    # NumberFilter filtra por valor numérico.
    # field_name='preco' diz em qual coluna do banco aplicar o filtro.
    # lookup_expr='gte' significa "maior ou igual" (>=).
    # Uso: GET /api/produtos/?preco_min=100 → retorna produtos com preço >= 100
    preco_min = django_filters.NumberFilter(field_name='preco', lookup_expr='gte')

    # lookup_expr='lte' significa "menor ou igual" (<=).
    # Uso: GET /api/produtos/?preco_max=500 → retorna produtos com preço <= 500
    # Combinando os dois: ?preco_min=100&preco_max=500 → faixa de preço
    preco_max = django_filters.NumberFilter(field_name='preco', lookup_expr='lte')

    # CharFilter filtra por texto.
    # lookup_expr='icontains' significa "contém, ignorando maiúsculas/minúsculas".
    # Uso: GET /api/produtos/?nome=note → retorna "Notebook", "Note 10", etc.
    # Diferente de 'exact' que exigiria o nome completo e exato.
    nome = django_filters.CharFilter(field_name='nome', lookup_expr='icontains')

    class Meta:
        model = Produto
        # Campos listados aqui usam filtro exato (=) automaticamente.
        # ativo=true filtra só produtos ativos.
        # categoria=1 filtra produtos da categoria com id=1.
        # Os campos preco_min, preco_max e nome são definidos acima com
        # lookups personalizados, por isso não precisam de configuração extra aqui.
        fields = ['ativo', 'categoria', 'preco_min', 'preco_max', 'nome']
