"""
urls.py (app produtos) — Mapeamento de URLs para views do app.

Este arquivo define QUAIS URLs existem dentro do prefixo /api/
(configurado em loja_api/urls.py).

Temos dois tipos de URL aqui:
  1. Geradas automaticamente pelo Router (para ViewSets)
  2. Mapeadas manualmente com path() (para APIViews)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriaViewSet,
    ProdutoViewSet,
    PedidoViewSet,
    EstatisticasView,
    BuscaGlobalView,
    LogoutView,
    CustomTokenObtainPairView,
)
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


# =============================================================================
# ROUTER — Geração automática de URLs para ViewSets
# =============================================================================
# O DefaultRouter cria automaticamente as URLs padrão REST para cada ViewSet registrado.
# Ao registrar 'produtos' com ProdutoViewSet, ele gera:
#
#   GET    /api/produtos/           → ProdutoViewSet.list()
#   POST   /api/produtos/           → ProdutoViewSet.create()
#   GET    /api/produtos/{id}/      → ProdutoViewSet.retrieve()
#   PUT    /api/produtos/{id}/      → ProdutoViewSet.update()
#   PATCH  /api/produtos/{id}/      → ProdutoViewSet.partial_update()
#   DELETE /api/produtos/{id}/      → ProdutoViewSet.destroy()
#   POST   /api/produtos/{id}/ativar/   → ProdutoViewSet.ativar()    (action customizada)
#   POST   /api/produtos/{id}/desativar/ → ProdutoViewSet.desativar() (action customizada)
#
# DefaultRouter também gera a API Root em GET /api/ listando todos os endpoints.
# SimpleRouter faz o mesmo, mas sem a API Root.

router = DefaultRouter()

# router.register(prefixo, ViewSet, basename)
# prefixo = parte da URL após /api/
# basename = prefixo dos nomes gerados (ex: 'produto-list', 'produto-detail')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'produtos', ProdutoViewSet, basename='produto')
router.register(r'pedidos', PedidoViewSet, basename='pedido')


# =============================================================================
# URL PATTERNS
# =============================================================================

urlpatterns = [
    # Inclui todas as URLs geradas automaticamente pelo router acima.
    # router.urls é uma lista de objetos URLPattern prontos para uso.
    path('', include(router.urls)),

    # -------------------------------------------------------------------------
    # URLs manuais — para endpoints que não são CRUD padrão
    # -------------------------------------------------------------------------

    # GET /api/estatisticas/ — resumo estatístico para admins
    # .as_view() converte a classe APIView em uma função compatível com Django URLs
    path('estatisticas/', EstatisticasView.as_view(), name='estatisticas'),

    # GET /api/busca/?q=termo — busca global em múltiplos models
    path('busca/', BuscaGlobalView.as_view(), name='busca-global'),

    # -------------------------------------------------------------------------
    # Autenticação JWT
    # -------------------------------------------------------------------------
    # POST /api/auth/token/ — faz login, retorna access_token + refresh_token
    # Usamos nossa view customizada que inclui username e email no payload
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # POST /api/auth/token/refresh/ — usa refresh_token para obter novo access_token
    # Necessário pois o access_token tem vida curta (60 min)
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # POST /api/auth/token/verify/ — verifica se um token é válido (sem renovar)
    # Útil para o frontend checar se ainda está autenticado
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # POST /api/auth/logout/ — invalida o refresh_token via blacklist
    path('auth/logout/', LogoutView.as_view(), name='logout'),
]
