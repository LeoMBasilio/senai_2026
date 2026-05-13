from django.db.models import Avg, Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
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


# --- Aula 4 - Ex 4: CategoriaViewSet completo ---
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    # Aula 4 - Ex 6: permissões diferenciadas por ação
    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


# --- Aula 4 - Ex 4 e 5: ProdutoViewSet com customizações ---
class ProdutoViewSet(viewsets.ModelViewSet):
    serializer_class = ProdutoSerializer
    filterset_class = ProdutoFilter
    search_fields = ['nome', 'descricao', 'tags']         # Aula 6 - Ex 3 e 5
    ordering_fields = ['preco', 'nome', 'criado_em']      # Aula 6 - Ex 3
    ordering = ['-criado_em']                              # padrão

    # Aula 4 - Ex 5: retorna apenas produtos ativos por padrão
    def get_queryset(self):
        return Produto.objects.filter(ativo=True)

    # Aula 4 - Ex 6: permissões diferenciadas por ação
    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    # Aula 4 - Ex 5: action customizada para ativar produto
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def ativar(self, request, pk=None):
        produto = self.get_object()
        produto.ativo = True
        produto.save()
        return Response({'status': 'Produto ativado.'}, status=status.HTTP_200_OK)

    # Action extra: desativar produto
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def desativar(self, request, pk=None):
        produto = self.get_object()
        produto.ativo = False
        produto.save()
        return Response({'status': 'Produto desativado.'}, status=status.HTTP_200_OK)


# --- Aula 4 - Desafio 7: endpoint de estatísticas ---
class EstatisticasView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        qs = Produto.objects.all()
        ativos = qs.filter(ativo=True)
        mais_caro = qs.order_by('-preco').values('nome', 'preco').first()
        preco_medio = ativos.aggregate(media=Avg('preco'))['media']

        return Response({
            'total_produtos': qs.count(),
            'total_ativos': ativos.count(),
            'preco_medio': round(float(preco_medio), 2) if preco_medio else 0,
            'produto_mais_caro': mais_caro,
        })


# --- Aula 5 - Ex 5: LogoutView com blacklist ---
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Logout realizado com sucesso.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'detail': 'Token inválido ou já invalidado.'}, status=status.HTTP_400_BAD_REQUEST)


# --- Aula 5 - Ex 6: View JWT customizada ---
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# --- Aula 6 - Desafio 7: busca global em múltiplos models ---
class BuscaGlobalView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        termo = request.query_params.get('q', '').strip()
        if not termo:
            return Response({'erro': 'Parâmetro "q" é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        produtos = Produto.objects.filter(Q(nome__icontains=termo))[:5]
        categorias = Categoria.objects.filter(Q(nome__icontains=termo))[:5]

        return Response({
            'produtos': ProdutoSerializer(produtos, many=True).data,
            'categorias': CategoriaSerializer(categorias, many=True).data,
        })


# --- Aula 4 - Desafio: ViewSet de Pedidos ---
class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Pedido.objects.filter(cliente=self.request.user).prefetch_related('itens__produto')

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        pedido = self.get_object()
        if pedido.status in ('enviado', 'entregue'):
            return Response(
                {'erro': 'Não é possível cancelar pedido já enviado ou entregue.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        pedido.status = 'pendente'
        pedido.save()
        return Response({'status': 'Pedido cancelado (voltou para pendente).'})
