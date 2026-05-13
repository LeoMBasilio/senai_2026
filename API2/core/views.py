# views.py — Define como a API responde às requisições HTTP.
# ViewSets agrupam todas as ações CRUD (listar, criar, detalhar, atualizar,
# deletar) em uma única classe, sem precisar criar uma view para cada rota.

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
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

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    def get_permissions(self):
        # Permissões diferenciadas por ação.
        # Leitura (list e retrieve) é pública — qualquer pessoa pode ver categorias.
        # Escrita (create, update, partial_update, destroy) exige autenticação.
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated()]


class ProdutoViewSet(viewsets.ModelViewSet):
    serializer_class = ProdutoSerializer

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
        # 'create', 'update', 'partial_update', 'destroy' ou o nome de
        # qualquer @action customizada definida nesta classe.

        if self.action == 'list':
            # Na listagem geral, retorna APENAS produtos ativos.
            # Produtos com ativo=False ficam ocultos da listagem pública.
            # select_related('categoria') faz um JOIN no banco, evitando
            # uma query extra para cada produto (problema N+1).
            return Produto.objects.filter(ativo=True).select_related('categoria')

        # Para todas as outras ações (retrieve, update, delete, ativar),
        # retorna todos os produtos, inclusive os inativos.
        # Isso é essencial para que a action 'ativar' consiga encontrar
        # um produto inativo pelo id e reativá-lo.
        return Produto.objects.all().select_related('categoria')

    def get_permissions(self):
        # get_permissions() é chamado pelo DRF antes de executar qualquer ação.
        # Retorna uma lista de instâncias de permissão (não classes — note os ()).
        # O DRF chama .has_permission() em cada uma; se alguma negar, retorna 401/403.

        # Ações de leitura são públicas: qualquer pessoa pode consultar produtos.
        # 'ativar' também exige autenticação por ser uma ação de escrita.
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]

        # Todas as demais ações (create, update, partial_update, destroy, ativar)
        # exigem que o usuário esteja autenticado com um JWT válido.
        return [IsAuthenticated()]

    # @action transforma um método comum em um endpoint extra do ViewSet.
    # detail=True → a URL inclui o {id} do objeto: /api/produtos/{id}/ativar/
    # detail=False → a URL seria na coleção: /api/produtos/ativar/ (sem id)
    # methods=["post"] → só aceita requisições POST neste endpoint.
    # O nome do método vira o sufixo da URL automaticamente.
    @action(detail=True, methods=['post'])
    def ativar(self, request, pk=None):
        # get_object() busca o produto pelo pk da URL e já aplica get_queryset().
        # Se o produto não existir, retorna 404 automaticamente.
        # Como get_queryset() retorna todos (inclusive inativos) para ações além
        # de 'list', conseguimos encontrar e reativar produtos inativos aqui.
        produto = self.get_object()

        # Atualiza só o campo 'ativo' sem mexer nos outros campos.
        # update_fields limita o UPDATE no banco a apenas essa coluna,
        # o que é mais eficiente do que um save() completo.
        produto.ativo = True
        produto.save(update_fields=['ativo'])

        # Serializa o produto atualizado para devolver no corpo da resposta.
        serializer = self.get_serializer(produto)

        # HTTP 200 OK indica que a operação foi executada com sucesso.
        return Response(serializer.data, status=status.HTTP_200_OK)
