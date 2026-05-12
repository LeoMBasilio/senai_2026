# settings.py — Arquivo de configuração central do projeto Django.
# Tudo que o projeto precisa saber para funcionar está aqui:
# banco de dados, apps instalados, autenticação, segurança, etc.

from pathlib import Path
# timedelta é usado para definir durações de tempo (ex: 60 minutos, 7 dias).
from datetime import timedelta

# BASE_DIR aponta para a pasta raiz do projeto (onde está o manage.py).
# É usada para construir outros caminhos de forma portátil entre sistemas operacionais.
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta usada pelo Django para assinar cookies, tokens CSRF, etc.
# Em produção NUNCA deixe essa chave hardcoded no código — use variável de ambiente.
SECRET_KEY = 'django-insecure-nm0hugw6vv*be2$v_zvdo((nsp43n5(u*-t9gs!i6crdh5&vcp'

# DEBUG=True exibe erros detalhados no navegador. Ótimo para desenvolvimento.
# Em produção deve ser False para não expor informações sensíveis.
DEBUG = True

# Lista de domínios que podem servir este projeto.
# Vazio em desenvolvimento pois DEBUG=True já libera localhost.
ALLOWED_HOSTS = []


INSTALLED_APPS = [
    # Apps padrão do Django — fornecem admin, autenticação, sessões, etc.
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Django REST Framework — transforma o projeto Django em uma API REST.
    # Fornece serializers, ViewSets, autenticação, permissões e muito mais.
    'rest_framework',

    # App de blacklist de tokens JWT.
    # Necessário para que o logout invalide o refresh token usado.
    # Quando BLACKLIST_AFTER_ROTATION=True, cada refresh token antigo
    # é gravado aqui e rejeitado se alguém tentar reutilizá-lo.
    'rest_framework_simplejwt.token_blacklist',

    # Biblioteca de filtros avançados para DRF.
    # Permite criar filtros com lookups como >=, <=, icontains, etc.
    'django_filters',

    # Nosso app com os models Categoria e Produto.
    'core',
]

# Configurações globais do Django REST Framework.
# Cada chave define o comportamento padrão para TODOS os endpoints da API.
REST_FRAMEWORK = {
    # Define como a API vai identificar quem está fazendo a requisição.
    # JWTAuthentication lê o header "Authorization: Bearer <token>" e
    # valida o token JWT para saber qual usuário está autenticado.
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    # Define o que um usuário autenticado (ou não) pode fazer.
    # IsAuthenticatedOrReadOnly:
    #   - Não autenticado → só pode fazer GET (leitura)
    #   - Autenticado → pode fazer POST, PUT, PATCH, DELETE (escrita)
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),

    # Filter backends definem quais tipos de filtro estão disponíveis globalmente.
    # DjangoFilterBackend → filtros exatos e customizados (?ativo=true, ?categoria=1)
    # SearchFilter         → busca textual (?search=notebook)
    # OrderingFilter       → ordenação (?ordering=preco ou ?ordering=-preco)
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],

    # Ativa paginação automática em todos os endpoints de listagem.
    # PageNumberPagination divide os resultados em páginas numeradas.
    # Use ?page=2 para acessar a segunda página.
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',

    # Quantos itens retornar por página quando o cliente não especifica.
    'PAGE_SIZE': 10,
}

# Configurações específicas da biblioteca SimpleJWT.
SIMPLE_JWT = {
    # O access token dura 60 minutos.
    # Após isso, o cliente precisa usar o refresh token para obter um novo.
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),

    # O refresh token dura 7 dias.
    # Enquanto ele for válido, o cliente pode obter novos access tokens
    # sem precisar digitar usuário e senha novamente.
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

    # A cada uso do refresh token, um NOVO refresh token é emitido.
    # O token antigo vai para a blacklist e não pode mais ser usado.
    # Isso impede que tokens roubados sejam reutilizados indefinidamente.
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Middlewares são funções que processam cada requisição antes de chegar
# na view e cada resposta antes de ser enviada ao cliente.
# A ordem importa — eles rodam em sequência.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Diz ao Django onde está o arquivo de URLs principal do projeto.
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

WSGI_APPLICATION = 'loja_api.wsgi.application'

# Banco de dados usado pelo projeto.
# SQLite é um arquivo local — ideal para desenvolvimento e testes.
# Em produção, seria trocado por PostgreSQL ou MySQL.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validadores de senha — exigem que as senhas atendam requisitos mínimos
# de segurança ao criar ou alterar uma senha de usuário.
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
