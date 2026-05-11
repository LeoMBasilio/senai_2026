# ============================================================
# views.py — Controla o que acontece em cada requisição HTTP
#
# A "view" é o cérebro da API: ela recebe a requisição,
# consulta o banco de dados, e devolve a resposta em JSON.
#
# Usamos ModelViewSet, que cria AUTOMATICAMENTE os 5 endpoints
# padrão de um CRUD com uma única classe:
#
#   GET    /api/produtos/        → lista todos os produtos
#   POST   /api/produtos/        → cria um novo produto
#   GET    /api/produtos/{id}/   → detalha um produto
#   PUT    /api/produtos/{id}/   → atualiza o produto inteiro
#   PATCH  /api/produtos/{id}/   → atualiza campos parcialmente
#   DELETE /api/produtos/{id}/   → remove o produto
# ============================================================

from rest_framework import viewsets, filters          # ferramentas de view e ordenação
from rest_framework.permissions import IsAuthenticated # exige usuário logado
from django_filters.rest_framework import DjangoFilterBackend # filtros por campo
from .models import Produto          # o model com a tabela do banco
from .serializers import ProdutoSerializer  # converte Produto <-> JSON
from .filters import ProdutoFilter   # filtros personalizados de preço/nome


class ProdutoViewSet(viewsets.ModelViewSet):

    # queryset → qual conjunto de dados a view vai usar.
    # Produto.objects.all() = busca TODOS os registros da tabela Produto.
    queryset = Produto.objects.all()

    # serializer_class → qual serializer vai converter os dados para JSON.
    serializer_class = ProdutoSerializer

    # permission_classes → quem pode acessar esses endpoints.
    # IsAuthenticated = apenas usuários com token JWT válido.
    # Sem token, a API devolve erro 401 (Não autorizado).
    permission_classes = [IsAuthenticated]

    # filter_backends → lista de "mecanismos de filtragem" ativos.
    # Cada um adiciona um tipo diferente de busca via URL.
    filter_backends = [
        DjangoFilterBackend,   # filtros por campo exato: ?ativo=true&preco_min=10
        filters.SearchFilter,  # busca textual:           ?search=cafe
        filters.OrderingFilter, # ordenação:              ?ordering=preco
    ]

    # filterset_class → usa os filtros personalizados definidos em filters.py
    filterset_class = ProdutoFilter

    # search_fields → em quais campos o ?search= vai pesquisar
    search_fields = ['nome', 'descricao']

    # ordering_fields → quais campos podem ser usados para ordenar
    ordering_fields = ['preco', 'nome', 'criado_em']

    # ordering → ordem padrão quando nenhum ?ordering= é informado.
    # O sinal "-" significa DECRESCENTE (mais recente primeiro).
    ordering = ['-criado_em']
