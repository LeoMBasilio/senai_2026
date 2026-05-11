import django_filters
from .models import Produto

class ProdutoFilter(django_filters.FilterSet):
    preco_min = django_filters.NumberFilter(
    field_name='preco', lookup_expr='gte')
    preco_max = django_filters.NumberFilter(
    field_name='preco', lookup_expr='lte')
    nome = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Produto
        fields = ['ativo', 'preco_min', 'preco_max', 'nome']