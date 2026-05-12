# urls.py — Arquivo central de rotas do projeto.
# Mapeia URLs para as views (ViewSets) que devem responder cada requisição.

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import CategoriaViewSet, ProdutoViewSet

# DefaultRouter gera automaticamente todas as rotas de um ViewSet.
# Sem ele, precisaríamos escrever path() para cada um dos 6 endpoints manualmente.
router = DefaultRouter()

# register() associa um prefixo de URL ao ViewSet.
# 'categorias' → gera /api/categorias/ e /api/categorias/{id}/
# 'produtos'   → gera /api/produtos/  e /api/produtos/{id}/
# basename é o nome base usado para referenciar as rotas (ex: reverse('categoria-list'))
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'produtos', ProdutoViewSet, basename='produto')

urlpatterns = [
    # Painel administrativo do Django — acesse /admin/ no navegador.
    path('admin/', admin.site.urls),

    # include(router.urls) injeta todas as rotas geradas pelo DefaultRouter
    # sob o prefixo 'api/'. O DefaultRouter também gera GET /api/ como
    # uma página índice listando todos os endpoints disponíveis.
    path('api/', include(router.urls)),

    # Endpoint para fazer login e receber os tokens JWT.
    # POST /api/auth/token/ com {"username": "...", "password": "..."}
    # Retorna {"access": "eyJ...", "refresh": "eyJ..."}
    # O token access deve ser enviado no header: Authorization: Bearer eyJ...
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Endpoint para renovar o access token sem precisar fazer login novamente.
    # O access token expira em 60 minutos (configurado no settings.py).
    # Quando expirar, envie o refresh token aqui para receber um novo access token.
    # POST /api/auth/token/refresh/ com {"refresh": "eyJ..."}
    # Retorna um novo {"access": "...", "refresh": "..."}
    # O refresh token antigo é adicionado à blacklist (token_blacklist) e
    # não pode mais ser usado — isso é o ROTATE_REFRESH_TOKENS em ação.
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
