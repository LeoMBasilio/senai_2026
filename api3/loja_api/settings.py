"""
settings.py — Arquivo central de configuração do Django.

Aqui ficam TODAS as configurações do projeto: banco de dados, apps instalados,
segurança, autenticação, etc. É o primeiro arquivo que o Django lê ao iniciar.
"""

from pathlib import Path
from datetime import timedelta  # usado para definir tempo de vida dos tokens JWT

# BASE_DIR aponta para a raiz do projeto (a pasta que contém manage.py).
# Path(__file__) = caminho deste arquivo (settings.py)
# .resolve().parent = pasta loja_api/
# .resolve().parent.parent = pasta raiz do projeto
# Usar BASE_DIR evita caminhos "hardcoded" como C:\Users\...
BASE_DIR = Path(__file__).resolve().parent.parent


# =============================================================================
# SEGURANÇA
# =============================================================================

# Chave secreta usada pelo Django para assinar cookies, tokens CSRF, etc.
# Em produção, NUNCA deixe esse valor no código — use variáveis de ambiente.
SECRET_KEY = 'django-insecure-d26@w+3e!nd5m509)fppp(6e5k8b4yd27(4r+a*k8-_#zp-f&u'

# DEBUG=True exibe erros detalhados no navegador. Útil em desenvolvimento.
# Em produção SEMPRE use DEBUG=False — expor stack trace é um risco de segurança.
DEBUG = True

# Lista de domínios que podem acessar esta API.
# [] = só aceita localhost em modo de desenvolvimento.
# Em produção: ALLOWED_HOSTS = ['meusite.com', 'www.meusite.com']
ALLOWED_HOSTS = []


# =============================================================================
# APPS INSTALADOS
# =============================================================================
# O Django só reconhece um app (models, views, etc.) se ele estiver aqui.
# A ordem importa para migrações: apps com dependências devem vir depois.

INSTALLED_APPS = [
    # Apps padrão do Django — não remova, são essenciais
    'django.contrib.admin',        # painel de administração em /admin/
    'django.contrib.auth',         # sistema de usuários, login, permissões
    'django.contrib.contenttypes', # sistema de tipos genéricos (usado por permissões)
    'django.contrib.sessions',     # armazenamento de sessão no banco
    'django.contrib.messages',     # sistema de mensagens flash (ex: "Salvo com sucesso!")
    'django.contrib.staticfiles',  # servir arquivos estáticos (CSS, JS, imagens)

    # Apps de terceiros instalados via pip
    'rest_framework',              # Django REST Framework — transforma Django em API REST
    'corsheaders',                 # permite que frontends de outros domínios consumam a API
    'django_filters',              # habilita filtros avançados nas QuerySets da API
    'rest_framework_simplejwt.token_blacklist',  # armazena tokens JWT invalidados (logout)

    # Nosso app criado com: python manage.py startapp produtos
    'produtos',
]


# =============================================================================
# MIDDLEWARE
# =============================================================================
# Middleware = camadas que processam TODA requisição antes de chegar na view
# e toda resposta antes de sair. A ORDEM É CRÍTICA.

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',          # força HTTPS, headers de segurança
    'corsheaders.middleware.CorsMiddleware',                  # DEVE vir antes do CommonMiddleware para funcionar
    'django.contrib.sessions.middleware.SessionMiddleware',   # habilita sessões por requisição
    'django.middleware.common.CommonMiddleware',              # normaliza URLs (ex: adiciona / no final)
    'django.middleware.csrf.CsrfViewMiddleware',              # proteção contra ataques CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware', # anexa o usuário logado em request.user
    'django.contrib.messages.middleware.MessageMiddleware',   # habilita mensagens flash
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # impede que a página seja embutida em iframes
]

# Diz ao Django qual arquivo de URLs usar como ponto de entrada
ROOT_URLCONF = 'loja_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Ponto de entrada para servidores web de produção (Gunicorn, uWSGI)
WSGI_APPLICATION = 'loja_api.wsgi.application'


# =============================================================================
# BANCO DE DADOS
# =============================================================================
# SQLite é um arquivo local — perfeito para desenvolvimento, não precisa instalar nada.
# Em produção, troque por PostgreSQL:
#   'ENGINE': 'django.db.backends.postgresql'
#   'NAME': 'nome_do_banco', 'USER': '...', 'PASSWORD': '...', 'HOST': 'localhost'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # arquivo criado na raiz do projeto
    }
}


# =============================================================================
# VALIDAÇÃO DE SENHAS
# =============================================================================
# O Django valida senhas automaticamente ao criar/alterar usuários.
# Cada validador abaixo aplica uma regra diferente:

AUTH_PASSWORD_VALIDATORS = [
    # Impede senhas similares ao nome do usuário
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    # Exige mínimo de 8 caracteres
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    # Bloqueia senhas comuns como "123456" ou "password"
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    # Impede senhas só com números
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# =============================================================================
# INTERNACIONALIZAÇÃO
# =============================================================================

LANGUAGE_CODE = 'en-us'  # idioma padrão do admin e mensagens do Django
TIME_ZONE = 'UTC'         # fuso horário para salvar datas no banco
USE_I18N = True           # habilita traduções
USE_TZ = True             # salva datas com timezone (evita bugs de horário)


STATIC_URL = 'static/'   # URL base para arquivos estáticos


# =============================================================================
# DJANGO REST FRAMEWORK (DRF)
# =============================================================================
# Configurações globais que se aplicam a TODOS os endpoints da API,
# a menos que a view sobreescreva individualmente.

REST_FRAMEWORK = {
    # Como o DRF identifica o usuário na requisição.
    # Dois métodos em paralelo — o DRF tenta cada um na ordem:
    #   1. JWTAuthentication: lê o header Authorization: Bearer <token>
    #      → usado por Postman, frontends, aplicações externas
    #   2. SessionAuthentication: lê o cookie de sessão do navegador
    #      → habilita o botão "Log in" da interface web do DRF
    #      → ao fazer login no /admin/ ou na tela de login do DRF,
    #        a sessão é criada e todos os endpoints passam a funcionar
    #        diretamente no navegador, sem precisar copiar tokens.
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

    # Permissão padrão para todos os endpoints:
    # - Usuário autenticado: pode ler E escrever
    # - Usuário anônimo: só pode ler (GET, HEAD, OPTIONS)
    # Views individuais podem sobrescrever com permission_classes = [...]
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],

    # Backends de filtro ativos em todos os ViewSets.
    # Cada backend adiciona um tipo de filtragem via query params na URL:
    # - DjangoFilterBackend: filtros exatos por campo (?ativo=true&categoria=1)
    # - SearchFilter: busca textual em múltiplos campos (?search=cafe)
    # - OrderingFilter: ordenação (?ordering=-preco)
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],

    # Classe de paginação usada por padrão em todos os ListViewSets.
    # Definida em produtos/pagination.py
    'DEFAULT_PAGINATION_CLASS': 'produtos.pagination.ProductPagination',
    'PAGE_SIZE': 12,  # itens por página se o cliente não especificar
}


# =============================================================================
# CORS — Cross-Origin Resource Sharing
# =============================================================================
# Por padrão, navegadores bloqueiam requisições de um domínio para outro.
# Ex: frontend em localhost:3000 chamando API em localhost:8000 seria bloqueado.
# CORS_ALLOW_ALL_ORIGINS=True libera qualquer origem — OK para desenvolvimento.
# Em produção, use: CORS_ALLOWED_ORIGINS = ['https://meufront.com']

CORS_ALLOW_ALL_ORIGINS = True


# =============================================================================
# JWT — JSON Web Token (Simple JWT)
# =============================================================================
# Configurações dos tokens de autenticação.
# Um token JWT tem duas partes: access (curta duração) e refresh (longa duração).
#
# Fluxo:
#   1. Cliente faz POST /auth/token/ com usuário e senha
#   2. Recebe access_token (60 min) e refresh_token (1 dia)
#   3. Usa access_token no header Authorization em cada requisição
#   4. Quando o access expira, usa o refresh_token para obter um novo par

SIMPLE_JWT = {
    # Tempo de vida do access token (usado em cada requisição autenticada)
    # Curto por segurança: se vazar, o dano é limitado a 60 minutos
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),

    # Tempo de vida do refresh token (usado para renovar o access)
    # Mais longo pois fica armazenado com mais cuidado pelo cliente
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),

    # A cada uso do refresh, gera um NOVO par de tokens.
    # Isso invalida o refresh anterior, dificultando roubo de sessão.
    'ROTATE_REFRESH_TOKENS': True,

    # Quando ROTATE_REFRESH_TOKENS=True, o refresh antigo vai para a blacklist.
    # Requer o app 'rest_framework_simplejwt.token_blacklist' em INSTALLED_APPS.
    'BLACKLIST_AFTER_ROTATION': True,

    # Tipo do token esperado no header Authorization.
    # O cliente envia: Authorization: Bearer eyJhbGci...
    'AUTH_HEADER_TYPES': ('Bearer',),
}
