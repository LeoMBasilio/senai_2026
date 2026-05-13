# Loja API

API REST de uma loja virtual construída com Django e Django REST Framework, desenvolvida como resolução da lista de exercícios **"Introdução a API com Django — Aulas 2 a 6"**.

## Tecnologias

- Python 3.14
- Django 6.0
- Django REST Framework 3.17
- Simple JWT 5.5 (autenticação por tokens)
- django-filter 25.2 (filtros avançados)
- django-cors-headers 4.9 (controle de CORS)
- SQLite (banco de dados de desenvolvimento)

---

## Instalação e execução

```bash
# 1. Criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Aplicar migrações
python manage.py migrate

# 4. Criar superusuário
python manage.py createsuperuser

# 5. Iniciar o servidor
python manage.py runserver
```

Acesse a API em: `http://localhost:8000/api/`  
Painel admin em: `http://localhost:8000/admin/`

---

## Endpoints disponíveis

| Método | URL | Descrição | Autenticação |
|--------|-----|-----------|--------------|
| GET | `/api/` | API Root — lista todos os endpoints | Não |
| GET | `/api/categorias/` | Lista categorias | Não |
| POST | `/api/categorias/` | Cria categoria | Sim |
| GET | `/api/categorias/{id}/` | Detalha categoria | Não |
| PUT/PATCH | `/api/categorias/{id}/` | Atualiza categoria | Sim |
| DELETE | `/api/categorias/{id}/` | Deleta categoria | Sim |
| GET | `/api/produtos/` | Lista produtos ativos | Não |
| POST | `/api/produtos/` | Cria produto | Sim |
| GET | `/api/produtos/{id}/` | Detalha produto | Não |
| PUT/PATCH | `/api/produtos/{id}/` | Atualiza produto | Sim |
| DELETE | `/api/produtos/{id}/` | Deleta produto | Sim |
| POST | `/api/produtos/{id}/ativar/` | Ativa produto | Sim |
| POST | `/api/produtos/{id}/desativar/` | Desativa produto | Sim |
| GET | `/api/pedidos/` | Lista pedidos do usuário logado | Sim |
| POST | `/api/pedidos/` | Cria pedido | Sim |
| GET | `/api/pedidos/{id}/` | Detalha pedido | Sim |
| POST | `/api/pedidos/{id}/cancelar/` | Cancela pedido | Sim |
| GET | `/api/estatisticas/` | Resumo estatístico | Admin |
| GET | `/api/busca/?q=termo` | Busca global | Não |
| POST | `/api/auth/token/` | Login — obtém tokens | Não |
| POST | `/api/auth/token/refresh/` | Renova access token | Não |
| POST | `/api/auth/token/verify/` | Verifica token | Não |
| POST | `/api/auth/logout/` | Logout (blacklist) | Sim |

---

## Autenticação na interface do DRF

Para testar endpoints autenticados direto no navegador, clique em **Log in** (canto superior direito de qualquer endpoint) e use as credenciais do superusuário.

Para Postman ou curl, use o header:
```
Authorization: Bearer <access_token>
```

Obtenha o token em `POST /api/auth/token/` com `{"username": "...", "password": "..."}`.

---

## Filtros disponíveis em `/api/produtos/`

| Query param | Exemplo | Comportamento |
|-------------|---------|---------------|
| `search` | `?search=cafe` | Busca em nome, descrição e tags |
| `ordering` | `?ordering=-preco` | Ordena por preço decrescente |
| `preco_min` | `?preco_min=10` | Preço maior ou igual a 10 |
| `preco_max` | `?preco_max=50` | Preço menor ou igual a 50 |
| `nome` | `?nome=cafe` | Nome contém "cafe" (sem diferenciar maiúsculas) |
| `ativo` | `?ativo=true` | Apenas ativos ou inativos |
| `categoria` | `?categoria=1` | Filtra pelo ID da categoria |
| `categoria__nome` | `?categoria__nome=bebidas` | Filtra pelo nome da categoria |
| `categoria__ativa` | `?categoria__ativa=true` | Filtra por categoria ativa/inativa |
| `page` | `?page=2` | Página 2 dos resultados |
| `page_size` | `?page_size=5` | 5 itens por página (máximo: 100) |

---

## Estrutura de arquivos

```
api3/
├── manage.py                  # CLI do Django (migrations, runserver, shell...)
├── requirements.txt           # Dependências do projeto
├── db.sqlite3                 # Banco de dados (gerado após migrate)
│
├── loja_api/                  # Configurações do projeto
│   ├── settings.py            # Configurações gerais (DRF, JWT, CORS, banco...)
│   ├── urls.py                # Roteador principal da aplicação
│   ├── wsgi.py                # Ponto de entrada para servidores de produção
│   └── asgi.py                # Ponto de entrada assíncrono (Channels, etc.)
│
└── produtos/                  # App principal da loja
    ├── models.py              # Tabelas do banco: Categoria, Produto, Pedido, ItemPedido
    ├── serializers.py         # Conversão Model ↔ JSON + validações
    ├── views.py               # Lógica dos endpoints (ViewSets e APIViews)
    ├── urls.py                # URLs do app (router + endpoints manuais)
    ├── filters.py             # Filtros customizados para produtos
    ├── pagination.py          # Paginação com campo total_pages
    ├── admin.py               # Registro dos models no painel /admin/
    └── migrations/            # Histórico de alterações no banco
```

---

## Mapeamento com os exercícios do PDF

### Aula 2 — Configurando o Ambiente

#### Exercício 4 — Criar ambiente completo do zero
> *"Crie uma pasta chamada 'loja_api' e entre nela, crie e ative o venv, instale Django, DRF e django-cors-headers..."*

| O que foi feito | Onde está |
|-----------------|-----------|
| Ambiente virtual com `python -m venv venv` | Pasta `venv/` na raiz |
| Instalação dos pacotes | `requirements.txt` |
| Criação do projeto com `django-admin startproject` | Pasta `loja_api/` |
| Criação do app com `python manage.py startapp` | Pasta `produtos/` |
| Migrações iniciais com `python manage.py migrate` | Pasta `produtos/migrations/` |

#### Exercício 5 — Configurar o settings.py
> *"Adicione os três apps necessários ao INSTALLED_APPS, configure REST_FRAMEWORK com IsAuthenticatedOrReadOnly, adicione o CorsMiddleware..."*

| Configuração | Onde está |
|--------------|-----------|
| `INSTALLED_APPS` com `rest_framework`, `corsheaders`, `django_filters`, `token_blacklist`, `produtos` | `loja_api/settings.py` — bloco INSTALLED_APPS |
| `REST_FRAMEWORK` com `IsAuthenticatedOrReadOnly` | `loja_api/settings.py` — bloco DRF |
| `CorsMiddleware` antes do `CommonMiddleware` | `loja_api/settings.py` — bloco MIDDLEWARE |
| `CORS_ALLOW_ALL_ORIGINS = True` | `loja_api/settings.py` — bloco CORS |

#### Exercício 6 — Criar superusuário e explorar o admin
> *"Execute createsuperuser com username 'admin' e senha segura..."*

| O que foi feito | Onde está |
|-----------------|-----------|
| Superusuário criado: `admin` / `Admin@1234` | Via `python manage.py createsuperuser` |
| Models registrados no admin | `produtos/admin.py` |
| API Root acessível em `/api/` | Configurado via `DefaultRouter` em `produtos/urls.py` |

---

### Aula 3 — Models e Serializers

#### Exercício 4 — Criar o Model Categoria e Produto com relacionamento
> *"Categoria: id, nome (único), descricao, ativa. Produto: id, nome, descricao, preco, estoque, ativo, criado_em, categoria (FK). Adicione on_delete=SET_NULL..."*

```python
# produtos/models.py

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    ativa = models.BooleanField(default=True)

class Produto(models.Model):
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, ...)
```

Arquivo: [produtos/models.py](produtos/models.py) — classes `Categoria` e `Produto`

#### Exercício 5 — Criar serializers para Categoria e Produto
> *"CategoriaSerializer: todos os campos, id como read_only. ProdutoSerializer: mostrando o nome da categoria (não o id)..."*

```python
# produtos/serializers.py

class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.SerializerMethodField()  # nome em vez do ID

    def get_categoria_nome(self, obj):
        return obj.categoria.nome if obj.categoria else None
```

Arquivo: [produtos/serializers.py](produtos/serializers.py) — classes `CategoriaSerializer` e `ProdutoSerializer`

#### Exercício 6 — Adicionar validações ao ProdutoSerializer
> *"validate_preco: maior que zero. validate_estoque: não negativo. validate: se ativo=True e estoque=0, levante erro..."*

```python
# produtos/serializers.py

def validate_preco(self, value):        # campo único
    if value <= 0: raise ...

def validate_estoque(self, value):      # campo único
    if value < 0: raise ...

def validate(self, data):               # validação cruzada
    if ativo and estoque == 0: raise ...
```

Arquivo: [produtos/serializers.py](produtos/serializers.py) — métodos `validate_*` dentro de `ProdutoSerializer`

#### Desafio 7 — Implementar Model Pedido com itens e total calculado
> *"Pedido: cliente (FK User), criado_em, status (choices). SerializerMethodField 'total' que soma preco * quantidade..."*

```python
# produtos/models.py
class Pedido(models.Model):
    STATUS_CHOICES = [('pendente','Pendente'), ('pago','Pago'), ...]
    status = models.CharField(choices=STATUS_CHOICES, ...)

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, ...)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(...)
```

| Parte | Arquivo |
|-------|---------|
| Models `Pedido` e `ItemPedido` | [produtos/models.py](produtos/models.py) |
| `PedidoSerializer` com `total` calculado | [produtos/serializers.py](produtos/serializers.py) |
| `ItemPedidoSerializer` com `subtotal` | [produtos/serializers.py](produtos/serializers.py) |

---

### Aula 4 — Views, ViewSets e Routers

#### Exercício 4 — Criar CategoriaViewSet e ProdutoViewSet completos
> *"Ambos herdam de ModelViewSet. Registre os dois no DefaultRouter. Inclua as URLs no urls.py principal sob o prefixo 'api/'..."*

```python
# produtos/views.py
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# produtos/urls.py
router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'produtos', ProdutoViewSet, basename='produto')
```

| Parte | Arquivo |
|-------|---------|
| `CategoriaViewSet` e `ProdutoViewSet` | [produtos/views.py](produtos/views.py) |
| `DefaultRouter` com registro dos ViewSets | [produtos/urls.py](produtos/urls.py) |
| Inclusão sob `/api/` | [loja_api/urls.py](loja_api/urls.py) |

#### Exercício 5 — Customizar o ProdutoViewSet
> *"Sobrescreva get_queryset() para retornar apenas produtos ativos. Adicione @action 'ativar' que seta produto.ativo=True..."*

```python
# produtos/views.py

def get_queryset(self):
    return Produto.objects.filter(ativo=True)  # só ativos por padrão

@action(detail=True, methods=['post'])
def ativar(self, request, pk=None):             # POST /api/produtos/{id}/ativar/
    produto = self.get_object()
    produto.ativo = True
    produto.save()
    return Response({'status': 'Produto ativado.'})
```

Arquivo: [produtos/views.py](produtos/views.py) — métodos `get_queryset`, `ativar` e `desativar` em `ProdutoViewSet`

#### Exercício 6 — Permissões diferenciadas por ação
> *"GET: permitir acesso sem autenticação. POST/PUT/DELETE: exigir autenticação. Sobrescreva get_permissions()..."*

```python
# produtos/views.py

def get_permissions(self):
    if self.action in ('list', 'retrieve'):
        return [permissions.AllowAny()]       # GET: livre
    return [permissions.IsAuthenticated()]    # escrita: precisa de token
```

Arquivo: [produtos/views.py](produtos/views.py) — método `get_permissions` em `CategoriaViewSet` e `ProdutoViewSet`

#### Desafio 7 — APIView customizada de estatísticas
> *"Endpoint: GET /api/estatisticas/. Retorne: total de produtos, total ativos, preço médio, produto mais caro. Permissão IsAdminUser..."*

```python
# produtos/views.py

class EstatisticasView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        preco_medio = Produto.objects.filter(ativo=True).aggregate(media=Avg('preco'))
        mais_caro = Produto.objects.order_by('-preco').values('nome', 'preco').first()
        ...
```

Arquivo: [produtos/views.py](produtos/views.py) — classe `EstatisticasView`

---

### Aula 5 — Autenticação JWT

#### Exercício 4 — Configurar e testar o fluxo completo de autenticação JWT
> *"Instale e configure djangorestframework-simplejwt. Adicione os três endpoints: /token/, /token/refresh/, /token/verify/..."*

```python
# loja_api/settings.py
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    ...
}

# produtos/urls.py
path('auth/token/', CustomTokenObtainPairView.as_view(), ...),
path('auth/token/refresh/', TokenRefreshView.as_view(), ...),
path('auth/token/verify/', TokenVerifyView.as_view(), ...),
```

| Parte | Arquivo |
|-------|---------|
| Configuração do `SIMPLE_JWT` | [loja_api/settings.py](loja_api/settings.py) — bloco JWT |
| Endpoints `/auth/token/`, `/auth/token/refresh/`, `/auth/token/verify/` | [produtos/urls.py](produtos/urls.py) |

#### Exercício 5 — Logout com blacklist
> *"Adicione token_blacklist ao INSTALLED_APPS. Crie a LogoutView que recebe o refresh token e chama token.blacklist()..."*

```python
# produtos/views.py

class LogoutView(APIView):
    def post(self, request):
        token = RefreshToken(request.data['refresh'])
        token.blacklist()   # insere na tabela BlacklistedToken do banco
```

| Parte | Arquivo |
|-------|---------|
| `rest_framework_simplejwt.token_blacklist` em `INSTALLED_APPS` | [loja_api/settings.py](loja_api/settings.py) |
| Classe `LogoutView` | [produtos/views.py](produtos/views.py) |
| URL `POST /api/auth/logout/` | [produtos/urls.py](produtos/urls.py) |

#### Exercício 6 — Customizar o payload do JWT
> *"Crie CustomTokenObtainPairSerializer. Sobrescreva get_token() e adicione token['username'] e token['email']..."*

```python
# produtos/serializers.py

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username   # dados extras no payload
        token['email'] = user.email
        return token
```

| Parte | Arquivo |
|-------|---------|
| `CustomTokenObtainPairSerializer` | [produtos/serializers.py](produtos/serializers.py) |
| `CustomTokenObtainPairView` | [produtos/views.py](produtos/views.py) |

---

### Aula 6 — Filtros, Busca e Paginação

#### Exercício 3 — Adicionar filtros completos ao ProdutoViewSet
> *"Crie um ProdutoFilter com: preco_min, preco_max, nome (icontains), ativo, categoria. Configure os três filter_backends. search_fields: nome e descricao. ordering_fields: preco, nome, criado_em..."*

```python
# produtos/filters.py
class ProdutoFilter(django_filters.FilterSet):
    preco_min = django_filters.NumberFilter(field_name='preco', lookup_expr='gte')
    preco_max = django_filters.NumberFilter(field_name='preco', lookup_expr='lte')
    nome      = django_filters.CharFilter(field_name='nome', lookup_expr='icontains')

# produtos/views.py (ProdutoViewSet)
filterset_class = ProdutoFilter
search_fields   = ['nome', 'descricao', 'tags']
ordering_fields = ['preco', 'nome', 'criado_em']
ordering        = ['-criado_em']
```

| Parte | Arquivo |
|-------|---------|
| Classe `ProdutoFilter` | [produtos/filters.py](produtos/filters.py) |
| `filterset_class`, `search_fields`, `ordering_fields` | [produtos/views.py](produtos/views.py) — `ProdutoViewSet` |
| `DEFAULT_FILTER_BACKENDS` global | [loja_api/settings.py](loja_api/settings.py) — bloco DRF |

#### Exercício 4 — Paginação customizada
> *"Crie uma classe ProductPagination com page_size=12, max_page_size=100. Adicione um campo extra 'total_pages'. Sobrescreva get_paginated_response()..."*

```python
# produtos/pagination.py

class ProductPagination(PageNumberPagination):
    page_size = 12
    max_page_size = 100

    def get_paginated_response(self, data):
        total_pages = math.ceil(self.page.paginator.count / self.get_page_size(self.request))
        return Response({'count': ..., 'total_pages': total_pages, 'results': data})
```

Arquivo: [produtos/pagination.py](produtos/pagination.py) — classe `ProductPagination`

#### Exercício 5 — Busca full-text com múltiplos campos
> *"Adicione campo 'tags' ao Model Produto. Configure search_fields para buscar em nome, descricao e tags..."*

```python
# produtos/models.py
tags = models.TextField(blank=True, help_text='Tags separadas por vírgula')

# produtos/views.py
search_fields = ['nome', 'descricao', 'tags']   # ?search=cafe busca nos três
```

| Parte | Arquivo |
|-------|---------|
| Campo `tags` no model | [produtos/models.py](produtos/models.py) — classe `Produto` |
| `search_fields` com `tags` | [produtos/views.py](produtos/views.py) — `ProdutoViewSet` |

#### Desafio 6 — Filtros aninhados por atributos de relacionamento
> *"Filtre produtos por nome da categoria: ?categoria__nome=bebidas. Use django_filters.CharFilter com field_name='categoria__nome'..."*

```python
# produtos/filters.py

categoria__nome  = django_filters.CharFilter(field_name='categoria__nome', lookup_expr='icontains')
categoria__ativa = django_filters.BooleanFilter(field_name='categoria__ativa')
# gera SQL: JOIN categoria WHERE categoria.nome ILIKE '%bebidas%'
```

Arquivo: [produtos/filters.py](produtos/filters.py) — campos `categoria__nome` e `categoria__ativa` em `ProdutoFilter`

#### Desafio 7 — Busca global em múltiplos models
> *"Endpoint: GET /api/busca/?q=termo. Busca simultânea em Produto.nome e Categoria.nome. Retorna no máximo 5 de cada. Use Q objects..."*

```python
# produtos/views.py

class BuscaGlobalView(APIView):
    def get(self, request):
        termo = request.query_params.get('q', '')
        produtos   = Produto.objects.filter(Q(nome__icontains=termo))[:5]
        categorias = Categoria.objects.filter(Q(nome__icontains=termo))[:5]
        return Response({'produtos': ..., 'categorias': ...})
```

| Parte | Arquivo |
|-------|---------|
| Classe `BuscaGlobalView` | [produtos/views.py](produtos/views.py) |
| URL `GET /api/busca/` | [produtos/urls.py](produtos/urls.py) |

---

## Credenciais padrão

| Usuário | Senha | Nível |
|---------|-------|-------|
| `admin` | `Admin@1234` | Superusuário (acesso total) |
