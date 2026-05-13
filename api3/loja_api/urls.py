"""
urls.py (raiz do projeto) — Roteador principal da aplicação.

Este arquivo é o "porteiro" da API: toda URL que chega no servidor
passa por aqui primeiro. Ele não processa as requisições diretamente,
apenas delega para os arquivos de URLs de cada app.

Analogia: é como um shopping center — este arquivo é a entrada principal,
e cada loja (app) tem seu próprio corredor de URLs interno.
"""

from django.contrib import admin
from django.urls import path, include  # include() encaminha para outro arquivo de URLs

urlpatterns = [
    # Painel de administração do Django — gerado automaticamente.
    # Acesse em: http://localhost:8000/admin/
    # Permite criar, editar e deletar qualquer dado do banco via interface web.
    path('admin/', admin.site.urls),

    # Todas as URLs que começam com "api/" são encaminhadas para produtos/urls.py.
    # Exemplo: /api/produtos/ → produtos/urls.py processa o restante (/produtos/)
    # Usar o prefixo "api/" é uma convenção para separar a API de outras rotas
    # (ex: frontend, documentação, etc.)
    path('api/', include('produtos.urls')),
]
