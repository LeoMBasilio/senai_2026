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

# --- Aula 4 - Ex 4: DefaultRouter com dois ViewSets ---
router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'produtos', ProdutoViewSet, basename='produto')
router.register(r'pedidos', PedidoViewSet, basename='pedido')

urlpatterns = [
    path('', include(router.urls)),

    # Aula 4 - Desafio 7: estatísticas
    path('estatisticas/', EstatisticasView.as_view(), name='estatisticas'),

    # Aula 6 - Desafio 7: busca global
    path('busca/', BuscaGlobalView.as_view(), name='busca-global'),

    # Aula 5 - Ex 4: endpoints JWT
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Aula 5 - Ex 5: logout com blacklist
    path('auth/logout/', LogoutView.as_view(), name='logout'),
]
