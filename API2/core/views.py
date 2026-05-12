# views.py — Define como a API responde às requisições HTTP.
# ViewSets agrupam todas as ações CRUD (listar, criar, detalhar, atualizar,
# deletar) em uma única classe, sem precisar criar uma view para cada rota.

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Categoria, Produto
from .serializers import CategoriaSerializer, ProdutoSerializer
from .filters import ProdutoFilter


class CategoriaViewSet(viewsets.ModelViewSet):
    # ModelViewSet gera automaticamente os 6 endpoints:
    # GET    /api/categorias/          → list (listar todas)
    # POST   /api/categorias/          → create (criar nova)
    # GET    /api/categorias/{id}/     → retrieve (detalhar uma)
    # PUT    /api/categorias/{id}/     → update (substituir completo)
    # PATCH  /api/categorias/{id}/     → partial_update (atualizar parcialmente)
    # DELETE /api/categorias/{id}/     → destroy (remover)

    # queryset diz de onde buscar os dados — aqui, todas as categorias.
    queryset = Categoria.objects.all()

    # serializer_class define qual serializer formata entrada e saída.
    serializer_class = CategoriaSerializer

    # AllowAny libera o endpoint para qualquer pessoa, sem autenticação.
    # Em produção seria trocado por IsAuthenticated ou IsAdminUser.
    permission_classes = [AllowAny]


class ProdutoViewSet(viewsets.ModelViewSet):
    serializer_class = ProdutoSerializer
    permission_classes = [AllowAny]

    # filterset_class conecta o ProdutoFilter a este ViewSet.
    # Isso ativa os filtros ?preco_min, ?preco_max, ?nome, ?ativo, ?categoria.
    filterset_class = ProdutoFilter

    # search_fields define em quais campos o parâmetro ?search busca.
    # Uso: GET /api/produtos/?search=notebook
    # O DRF procura "notebook" em nome E em descricao.
    search_fields = ['nome', 'descricao']

    # ordering_fields lista os campos em que o cliente pode ordenar.
    # Uso: GET /api/produtos/?ordering=preco (crescente)
    #      GET /api/produtos/?ordering=-preco (decrescente, com o hífen)
    ordering_fields = ['preco', 'estoque', 'nome']

    # ordering define a ordenação padrão quando o cliente não especifica nenhuma.
    ordering = ['nome']

    def get_queryset(self):
        # Sobrescrevemos get_queryset para ter comportamento diferente
        # dependendo da ação (action) que está sendo executada.

        # self.action contém o nome da ação atual: 'list', 'retrieve',
        # 'create', 'update', 'partial_update' ou 'destroy'.

        if self.action == 'list':
            # Na listagem geral, retorna APENAS produtos ativos.
            # Produtos com ativo=False ficam ocultos da listagem pública.
            # select_related('categoria') faz um JOIN no banco, evitando
            # uma query extra para cada produto (problema N+1).
            return Produto.objects.filter(ativo=True).select_related('categoria')

        # Para todas as outras ações (retrieve, update, delete), retorna
        # todos os produtos, inclusive os inativos.
        # Isso permite que o admin atualize ou reative um produto inativo
        # acessando diretamente o endpoint /api/produtos/{id}/.
        return Produto.objects.all().select_related('categoria')
