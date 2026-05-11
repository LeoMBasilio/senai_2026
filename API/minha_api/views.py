from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Produto
from .serializers import ProdutoSerializer
from .filters import ProdutoFilter

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated]


    filter_backends = [
        DjangoFilterBackend, # ?ativo=true&preco;_min=10
        filters.SearchFilter, # ?search=cafe
        filters.OrderingFilter, # ?ordering=preco
    ]

    filterset_class = ProdutoFilter
    search_fields = ['nome', 'descricao']
    ordering_fields = ['preco', 'nome', 'criado_em']
    ordering = ['-criado_em'] # padrão
