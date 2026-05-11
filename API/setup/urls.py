# ============================================================
# urls.py — Mapa de endereços (rotas) da API
#
# Define QUAIS URLs existem e QUAL view responde a cada uma.
# É como uma tabela de endereços:
#
#   URL acessada              →  Quem responde
#   /admin/                   →  Painel administrativo do Django
#   /api/produtos/            →  ProdutoViewSet (CRUD de produtos)
#   /api/token/               →  Login — gera o token JWT
#   /api/token/refresh/       →  Renova o token quando ele expira
#   /api/token/verify/        →  Verifica se um token ainda é válido
# ============================================================

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter  # cria URLs automaticamente
from minha_api.views import ProdutoViewSet

# Importa as views prontas do SimpleJWT para autenticação
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # POST com usuário+senha → retorna access + refresh token
    TokenRefreshView,     # POST com refresh token  → retorna novo access token
    TokenVerifyView,      # POST com qualquer token → confirma se é válido
)

# ----------------------------------------------------------
# Router — gera as URLs do CRUD automaticamente
# ----------------------------------------------------------
# DefaultRouter lê o ViewSet e cria todas as rotas necessárias.
# Com uma linha, criamos 6 endpoints diferentes (list, create,
# retrieve, update, partial_update, destroy).
router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet, basename='produtos')
# Resultado: /api/produtos/ e /api/produtos/{id}/

# ----------------------------------------------------------
# urlpatterns — lista oficial de todas as URLs do projeto
# ----------------------------------------------------------
urlpatterns = [
    # Painel de administração do Django (interface web para gerenciar dados)
    path('admin/', admin.site.urls),

    # include(router.urls) → adiciona todas as URLs geradas pelo router
    # O prefixo 'api/' aparece em todas: /api/produtos/, /api/produtos/1/, etc.
    path('api/', include(router.urls)),

    # --- Endpoints de autenticação JWT ---

    # Login: envie POST com {"username": "...", "password": "..."}
    # Recebe: {"access": "<token>", "refresh": "<token>"}
    path('api/token/', TokenObtainPairView.as_view()),

    # Renovar token: envie POST com {"refresh": "<token>"}
    # Recebe: {"access": "<novo token>"}
    # (o access token dura 2h; o refresh dura 7 dias)
    path('api/token/refresh/', TokenRefreshView.as_view()),

    # Verificar token: envie POST com {"token": "<token>"}
    # Recebe: 200 OK se válido, 401 se inválido/expirado
    path('api/token/verify/', TokenVerifyView.as_view()),
]
