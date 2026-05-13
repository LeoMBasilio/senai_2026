import django_filters
from .models import Produto


# --- Aula 6 - Ex 3: Filtro completo para Produto ---
class ProdutoFilter(django_filters.FilterSet):
    preco_min = django_filters.NumberFilter(field_name='preco', lookup_expr='gte')
    preco_max = django_filters.NumberFilter(field_name='preco', lookup_expr='lte')
    nome = django_filters.CharFilter(field_name='nome', lookup_expr='icontains')

    # Aula 6 - Desafio 6: filtros por atributos de relacionamento
    categoria__nome = django_filters.CharFilter(field_name='categoria__nome', lookup_expr='icontains')
    categoria__ativa = django_filters.BooleanFilter(field_name='categoria__ativa')

    class Meta:
        model = Produto
        fields = ['ativo', 'categoria', 'preco_min', 'preco_max', 'nome']
