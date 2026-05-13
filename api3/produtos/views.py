"""
views.py — As "funções" que processam as requisições e retornam respostas.

Uma view recebe uma requisição HTTP (GET, POST, PUT, DELETE...),
executa a lógica necessária (consulta banco, valida dados, etc.)
e retorna uma resposta HTTP com status code e dados JSON.

Tipos de view usados aqui:
  - ModelViewSet: gera automaticamente os 5 endpoints CRUD (list, create,
    retrieve, update, destroy) com poucas linhas de código.
  - APIView: view manual para endpoints que não seguem o padrão CRUD.
"""

from django.db.models import Avg, Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action    # para criar endpoints extras em ViewSets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Categoria, Produto, Pedido
from .serializers import (
    CategoriaSerializer,
    ProdutoSerializer,
    PedidoSerializer,
    CustomTokenObtainPairSerializer,
)
from .filters import ProdutoFilter


# =============================================================================
# CATEGORIA
# =============================================================================

class CategoriaViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo para categorias.

    ModelViewSet herda de todas as Mixins do DRF e gera automaticamente:
      GET    /api/categorias/       → list()     → lista todas as categorias
      POST   /api/categorias/       → create()   → cria nova categoria
      GET    /api/categorias/{id}/  → retrieve() → detalha uma categoria
      PUT    /api/categorias/{id}/  → update()   → atualiza completamente
      PATCH  /api/categorias/{id}/  → partial_update() → atualiza parcialmente
      DELETE /api/categorias/{id}/  → destroy()  → deleta a categoria
    """

    # queryset define QUAIS objetos este ViewSet opera.
    # .all() retorna todos os registros do banco por padrão.
    queryset = Categoria.objects.all()

    # serializer_class define como os dados são convertidos para/de JSON
    serializer_class = CategoriaSerializer

    def get_permissions(self):
        """
        Permissões diferenciadas por ação (tipo de requisição).

        self.action é uma string com o nome da ação atual:
        'list', 'retrieve', 'create', 'update', 'partial_update', 'destroy'

        AllowAny = qualquer um pode acessar (nem precisa estar logado)
        IsAuthenticated = só usuários com token válido podem acessar

        Por que diferenciar?
        Leitura (GET) é pública — qualquer visitante pode ver categorias.
        Escrita (POST/PUT/DELETE) é protegida — só quem está logado pode modificar.
        """
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


# =============================================================================
# PRODUTO
# =============================================================================

class ProdutoViewSet(viewsets.ModelViewSet):
    """
    ViewSet de produtos com filtros, busca, ordenação e ações customizadas.
    """

    serializer_class = ProdutoSerializer

    # Vincula a classe de filtros definida em filters.py.
    # O DjangoFilterBackend vai usar essa classe para processar query params.
    filterset_class = ProdutoFilter

    # Campos onde o SearchFilter vai buscar quando o cliente usa ?search=termo
    # O SearchFilter faz busca case-insensitive "contém" em todos os campos listados.
    # Ex: ?search=cafe → busca 'cafe' em nome, descricao E tags simultaneamente
    search_fields = ['nome', 'descricao', 'tags']

    # Campos que o cliente pode usar para ordenar com ?ordering=campo
    # Ex: ?ordering=preco → crescente, ?ordering=-preco → decrescente (- inverte)
    ordering_fields = ['preco', 'nome', 'criado_em']

    # Ordenação padrão quando o cliente não especifica ?ordering=
    # -criado_em = mais recentes primeiro (- significa DESC no SQL)
    ordering = ['-criado_em']

    def get_queryset(self):
        """
        Sobrescreve o queryset padrão para retornar APENAS produtos ativos.

        Por que sobrescrever em vez de usar queryset = Produto.objects.filter(ativo=True)?
        Porque queryset = ... é avaliado UMA vez quando a classe é carregada.
        get_queryset() é chamado em CADA requisição, permitindo lógica dinâmica
        (ex: filtrar por usuário logado, como fazemos no PedidoViewSet).

        Produtos inativos ficam "invisíveis" para a API pública, mas ainda
        existem no banco — o admin pode reativá-los.
        """
        return Produto.objects.filter(ativo=True)

    def get_permissions(self):
        """Mesma lógica do CategoriaViewSet: leitura pública, escrita autenticada."""
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def ativar(self, request, pk=None):
        """
        Action customizada: endpoint extra além do CRUD padrão.

        @action(detail=True) = opera em um objeto específico → gera URL: /api/produtos/{id}/ativar/
        @action(detail=False) = opera na coleção → geraria URL: /api/produtos/ativar/

        methods=['post'] = só aceita POST (semântica correta: é uma ação, não uma busca)

        self.get_object() busca o produto pelo {id} da URL e aplica permissões
        automaticamente (levanta 404 se não existir, 403 se não tiver permissão).
        """
        produto = self.get_object()
        produto.ativo = True
        produto.save()
        return Response({'status': 'Produto ativado.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def desativar(self, request, pk=None):
        """Action para desativar um produto — soft delete (não remove do banco)."""
        produto = self.get_object()
        produto.ativo = False
        produto.save()
        return Response({'status': 'Produto desativado.'}, status=status.HTTP_200_OK)


# =============================================================================
# ESTATÍSTICAS
# =============================================================================

class EstatisticasView(APIView):
    """
    Endpoint de relatório que não se encaixa no padrão CRUD.
    Usa APIView pois precisamos de lógica manual — um ViewSet seria excessivo.

    Só administradores têm acesso (IsAdminUser verifica user.is_staff=True).
    """

    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        """
        Processa requisições GET para /api/estatisticas/
        Retorna um resumo dos produtos do sistema.
        """
        # qs = QuerySet com TODOS os produtos (ativos e inativos)
        qs = Produto.objects.all()

        # Filtro adicional para contar apenas os ativos
        ativos = qs.filter(ativo=True)

        # .order_by('-preco') = DESC por preço. .values() retorna dicionário,
        # não objeto Model. .first() pega o primeiro resultado (ou None).
        mais_caro = qs.order_by('-preco').values('nome', 'preco').first()

        # .aggregate() faz cálculos no banco (SQL: SELECT AVG(preco)).
        # Mais eficiente do que trazer todos os registros e calcular em Python.
        # Retorna um dicionário: {'media': Decimal('45.90')}
        preco_medio = ativos.aggregate(media=Avg('preco'))['media']

        return Response({
            'total_produtos': qs.count(),
            'total_ativos': ativos.count(),
            # round() com 2 casas para exibir como dinheiro. Converte Decimal→float.
            'preco_medio': round(float(preco_medio), 2) if preco_medio else 0,
            'produto_mais_caro': mais_caro,
        })


# =============================================================================
# LOGOUT
# =============================================================================

class LogoutView(APIView):
    """
    Endpoint de logout via blacklist de refresh token.

    Por que precisamos de logout se JWT é stateless?
    O JWT em si não tem "logout" — um token válido sempre funciona até expirar.
    A blacklist é uma tabela no banco que guarda tokens invalidados.
    A cada requisição autenticada, o DRF verifica se o token está na blacklist.

    Fluxo do logout:
      1. Cliente envia o refresh token no body: {"refresh": "eyJ..."}
      2. O token é adicionado à blacklist no banco
      3. Qualquer tentativa futura de usar esse refresh retorna 401
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            # RefreshToken(string) → reconstrói o objeto token a partir da string JWT
            token = RefreshToken(refresh_token)
            # blacklist() insere o token na tabela OutstandingToken + BlacklistedToken
            token.blacklist()
            return Response({'detail': 'Logout realizado com sucesso.'}, status=status.HTTP_200_OK)
        except Exception:
            # Token pode ser inválido (malformado) ou já estar na blacklist
            return Response(
                {'detail': 'Token inválido ou já invalidado.'},
                status=status.HTTP_400_BAD_REQUEST
            )


# =============================================================================
# LOGIN JWT CUSTOMIZADO
# =============================================================================

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Substitui a view padrão de login para usar nosso serializer customizado.
    O serializer adiciona username e email no payload do JWT.

    Basta sobrescrever serializer_class — toda a lógica de autenticação
    (verificar usuário/senha, gerar tokens) vem da classe pai.
    """
    serializer_class = CustomTokenObtainPairSerializer


# =============================================================================
# BUSCA GLOBAL
# =============================================================================

class BuscaGlobalView(APIView):
    """
    Endpoint de busca que pesquisa em múltiplos models ao mesmo tempo.
    URL: GET /api/busca/?q=termo

    Por que não usar o SearchFilter do DRF aqui?
    O SearchFilter opera em um único model por ViewSet.
    Aqui precisamos buscar em Produto E Categoria simultaneamente — isso
    requer lógica manual com APIView.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # request.query_params é um dicionário com os query params da URL.
        # .get('q', '') retorna '' se o parâmetro não for enviado.
        # .strip() remove espaços em branco nas bordas.
        termo = request.query_params.get('q', '').strip()

        if not termo:
            return Response(
                {'erro': 'Parâmetro "q" é obrigatório.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Q() = objeto de query que permite combinar filtros com OR (|) e AND (&).
        # Aqui usamos apenas icontains, mas poderíamos fazer:
        # Q(nome__icontains=termo) | Q(descricao__icontains=termo)
        # para buscar em mais campos com uma única query.
        # [:5] limita o resultado a 5 itens de cada tipo (evita respostas gigantes)
        produtos = Produto.objects.filter(Q(nome__icontains=termo))[:5]
        categorias = Categoria.objects.filter(Q(nome__icontains=termo))[:5]

        return Response({
            # many=True serializa uma lista de objetos (QuerySet)
            'produtos': ProdutoSerializer(produtos, many=True).data,
            'categorias': CategoriaSerializer(categorias, many=True).data,
        })


# =============================================================================
# PEDIDOS
# =============================================================================

class PedidoViewSet(viewsets.ModelViewSet):
    """
    ViewSet de pedidos com isolamento por usuário.
    Cada usuário só vê e gerencia seus próprios pedidos.
    """

    serializer_class = PedidoSerializer
    # Todos os endpoints exigem autenticação — não faz sentido ver pedidos sem login
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filtra pedidos pelo usuário logado.
        request.user é preenchido automaticamente pelo middleware de autenticação.

        prefetch_related('itens__produto') faz JOIN antecipado para carregar
        os itens e produtos de uma vez. Sem isso, para cada pedido o Django
        faria uma query extra para buscar os itens (problema N+1).
        """
        return Pedido.objects.filter(
            cliente=self.request.user
        ).prefetch_related('itens__produto')

    def perform_create(self, serializer):
        """
        Chamado pelo create() após validar os dados.
        Injeta o usuário logado como 'cliente' automaticamente.
        O cliente não precisa (nem deve) enviar o campo 'cliente' no body.
        """
        serializer.save(cliente=self.request.user)

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """
        Action customizada: POST /api/pedidos/{id}/cancelar/
        Verifica se o pedido ainda pode ser cancelado antes de agir.

        Regra de negócio: pedidos já enviados ou entregues não podem ser cancelados.
        """
        pedido = self.get_object()

        if pedido.status in ('enviado', 'entregue'):
            return Response(
                {'erro': 'Não é possível cancelar pedido já enviado ou entregue.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        pedido.status = 'pendente'
        pedido.save()
        return Response({'status': 'Pedido cancelado (voltou para pendente).'})
