from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from minha_api.views import ProdutoViewSet

from rest_framework_simplejwt.views import (
TokenObtainPairView, TokenRefreshView, TokenVerifyView)

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet, basename='produtos')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/token/verify/', TokenVerifyView.as_view()),
]
