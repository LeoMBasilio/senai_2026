# ============================================================
# settings.py — Configurações gerais do projeto Django
#
# É aqui que configuramos tudo que o projeto precisa para
# funcionar: banco de dados, apps instalados, segurança, etc.
# ============================================================

from pathlib import Path

# BASE_DIR aponta para a pasta raiz do projeto.
# Usamos ele para construir caminhos de arquivos de forma segura
# em qualquer sistema operacional (Windows, Linux, Mac).
BASE_DIR = Path(__file__).resolve().parent.parent


# ----------------------------------------------------------
# Segurança
# ----------------------------------------------------------

# Chave secreta usada para criptografar sessões e tokens.
# NUNCA compartilhe essa chave em produção!
SECRET_KEY = 'django-insecure-fg(zv806tsja=v4*4$0e-rycn9*!v0uge9j_k^*q8me=&j7qoq'

# DEBUG=True → mostra erros detalhados na tela (ótimo para desenvolvimento).
# Em produção, deve ser False para não expor informações sensíveis.
DEBUG = True

# Lista de domínios que podem acessar o projeto.
# Vazio = só localhost pode acessar (ok para desenvolvimento).
ALLOWED_HOSTS = []


# ----------------------------------------------------------
# Apps instalados
# ----------------------------------------------------------
# Django é modular: cada funcionalidade é um "app".
# Precisamos listar todos os apps que o projeto usa.
INSTALLED_APPS = [
    'django.contrib.admin',        # painel de administração web
    'django.contrib.auth',         # sistema de usuários e login
    'django.contrib.contenttypes', # infraestrutura interna do Django
    'django.contrib.sessions',     # gerenciamento de sessões
    'django.contrib.messages',     # sistema de mensagens flash
    'django.contrib.staticfiles',  # arquivos estáticos (CSS, JS, imagens)
    'rest_framework',              # Django REST Framework — base da nossa API
    'rest_framework_simplejwt',    # autenticação via token JWT
    'django_filters',              # filtros avançados por parâmetros na URL
    'minha_api',                   # nosso app com os produtos
]


# ----------------------------------------------------------
# Configurações do Django REST Framework
# ----------------------------------------------------------
REST_FRAMEWORK = {

    # Como a API identifica QUEM está fazendo a requisição.
    # JWTAuthentication → lê o token Bearer no header Authorization.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],

    # O que é necessário para ACESSAR os endpoints.
    # IsAuthenticated → exige que o usuário esteja logado (tenha token válido).
    # Sem isso, qualquer um poderia acessar a API sem se identificar.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    # Mecanismo padrão de filtragem usado em todos os ViewSets.
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],

    # Paginação → divide a lista de resultados em páginas.
    # Sem paginação, uma requisição GET poderia retornar milhares de itens.
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',

    # Quantos itens aparecem por página.
    # Ex: /api/produtos/?page=2 → retorna os itens 11 a 20.
    'PAGE_SIZE': 10,
}


# ----------------------------------------------------------
# Configurações do SimpleJWT (tokens de autenticação)
# ----------------------------------------------------------
from datetime import timedelta

SIMPLE_JWT = {
    # ACCESS_TOKEN_LIFETIME → por quanto tempo o token de acesso é válido.
    # Após 2 horas, o usuário precisa usar o refresh token para renovar.
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),

    # REFRESH_TOKEN_LIFETIME → por quanto tempo o token de renovação é válido.
    # O usuário pode renovar o access token por até 7 dias sem fazer login novamente.
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

    # ROTATE_REFRESH_TOKENS → a cada renovação, gera um NOVO refresh token.
    # Isso aumenta a segurança: o token antigo não funciona mais.
    'ROTATE_REFRESH_TOKENS': True,

    # BLACKLIST_AFTER_ROTATION → o refresh token antigo vai para uma lista negra.
    # Garante que não possa ser reutilizado mesmo que alguém o tenha roubado.
    'BLACKLIST_AFTER_ROTATION': True,
}


# ----------------------------------------------------------
# Middlewares — camadas de processamento de cada requisição
# ----------------------------------------------------------
# Cada requisição passa por esses middlewares em ordem,
# antes de chegar na view e depois antes de retornar a resposta.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',             # proteções de segurança HTTP
    'django.contrib.sessions.middleware.SessionMiddleware',      # gerencia sessões de usuário
    'django.middleware.common.CommonMiddleware',                 # normaliza URLs (ex: adiciona barra final)
    'django.middleware.csrf.CsrfViewMiddleware',                 # proteção contra CSRF (formulários)
    'django.contrib.auth.middleware.AuthenticationMiddleware',   # injeta o usuário na requisição
    'django.contrib.messages.middleware.MessageMiddleware',      # mensagens flash entre requisições
    'django.middleware.clickjacking.XFrameOptionsMiddleware',    # proteção contra clickjacking
]

# Arquivo de URLs principal do projeto
ROOT_URLCONF = 'setup.urls'

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

WSGI_APPLICATION = 'setup.wsgi.application'


# ----------------------------------------------------------
# Banco de dados
# ----------------------------------------------------------
# SQLite → banco de dados simples em arquivo, ótimo para aprender.
# Em produção usaríamos PostgreSQL ou MySQL.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # arquivo criado na pasta raiz
    }
}


# ----------------------------------------------------------
# Validações de senha
# ----------------------------------------------------------
# Regras que a senha do usuário precisa seguir ao ser cadastrada.
AUTH_PASSWORD_VALIDATORS = [
    {
        # Não pode ser parecida com nome de usuário, email, etc.
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # Mínimo de 8 caracteres
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # Não pode ser uma senha comum (ex: "123456", "password")
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # Não pode ser só números
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ----------------------------------------------------------
# Internacionalização
# ----------------------------------------------------------
LANGUAGE_CODE = 'en-us'  # idioma padrão
TIME_ZONE = 'UTC'        # fuso horário (use 'America/Sao_Paulo' se quiser horário BR)
USE_I18N = True          # ativa suporte a tradução de textos
USE_TZ = True            # datas sempre armazenadas com fuso horário


# ----------------------------------------------------------
# Arquivos estáticos (CSS, JavaScript, imagens)
# ----------------------------------------------------------
STATIC_URL = 'static/'
