"""
models.py — Define a estrutura do banco de dados usando classes Python.

No Django, cada classe que herda de models.Model vira uma TABELA no banco.
Cada atributo da classe vira uma COLUNA dessa tabela.
O Django cuida de criar o SQL — você não precisa escrever CREATE TABLE.

Fluxo:
  1. Você define/altera um model aqui
  2. Roda: python manage.py makemigrations  → gera o arquivo de migração
  3. Roda: python manage.py migrate         → aplica a mudança no banco
"""

from django.db import models
from django.contrib.auth.models import User  # modelo de usuário padrão do Django


# =============================================================================
# CATEGORIA
# =============================================================================

class Categoria(models.Model):
    """
    Representa uma categoria de produtos (ex: Bebidas, Alimentos).
    Usada para agrupar produtos e permitir filtros por categoria.
    """

    # CharField = coluna VARCHAR no banco. max_length é obrigatório.
    # unique=True cria um índice UNIQUE — o banco rejeita nomes repetidos.
    nome = models.CharField(max_length=100, unique=True)

    # TextField = coluna TEXT — sem limite de tamanho, ideal para textos longos.
    # blank=True significa que o campo é OPCIONAL nos formulários/serializers.
    # (null=True não é necessário para TextField — Django salva string vazia)
    descricao = models.TextField(blank=True)

    # BooleanField = coluna BOOLEAN. default=True significa que toda nova
    # categoria nasce ativa sem precisar informar o campo.
    ativa = models.BooleanField(default=True)

    def __str__(self):
        # Método especial que define como o objeto aparece como string.
        # Usado no admin do Django e no shell. Ex: str(categoria) → "Bebidas"
        return self.nome


# =============================================================================
# PRODUTO
# =============================================================================

class Produto(models.Model):
    """
    Representa um produto da loja.
    Tem relacionamento com Categoria (muitos produtos para uma categoria).
    """

    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)

    # DecimalField = coluna DECIMAL — ideal para dinheiro pois evita erros
    # de arredondamento do float. max_digits=total de dígitos, decimal_places=casas decimais.
    # Ex: 1.299,90 tem 6 dígitos + 2 casas = max_digits=10 é mais que suficiente.
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    # IntegerField = coluna INTEGER. default=0 permite criar produto sem estoque.
    estoque = models.IntegerField(default=0)

    ativo = models.BooleanField(default=True)

    # auto_now_add=True preenche o campo AUTOMATICAMENTE com a data/hora atual
    # apenas na criação do objeto. Nunca é alterado depois.
    # Por isso não precisamos passar esse valor ao criar um produto.
    criado_em = models.DateTimeField(auto_now_add=True)

    # ForeignKey = relacionamento Muitos-para-Um (N:1).
    # Muitos produtos podem pertencer a UMA categoria.
    # on_delete=SET_NULL: se a categoria for deletada, o campo vira NULL
    #   (em vez de deletar o produto junto — CASCADE — ou dar erro — PROTECT)
    # null=True: permite que o campo seja NULL no banco
    # blank=True: permite que o campo seja vazio nos formulários/serializers
    # related_name='produtos': permite acessar os produtos de uma categoria
    #   com: categoria.produtos.all() — sem isso, seria categoria.produto_set.all()
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produtos'
    )

    # Campo de texto livre para tags separadas por vírgula.
    # Ex: "cafe,bebida,premium,organico"
    # Isso permite busca textual pelo SearchFilter da Aula 6.
    # Uma alternativa mais robusta seria uma tabela separada de tags (ManyToMany).
    tags = models.TextField(blank=True, help_text='Tags separadas por vírgula')

    def __str__(self):
        return self.nome


# =============================================================================
# PEDIDO
# =============================================================================

class Pedido(models.Model):
    """
    Representa um pedido feito por um cliente.
    Um pedido contém vários itens (produtos + quantidade).

    Por que não usar ManyToManyField diretamente?
    Porque precisamos armazenar informações EXTRAS no relacionamento
    (quantidade e preço no momento da compra). Usamos uma tabela intermediária
    explícita: ItemPedido.
    """

    # Lista de tuplas (valor_no_banco, label_legível).
    # O Django valida que o status só aceita esses valores.
    # Armazena 'pendente' no banco, mas exibe "Pendente" no admin/formulários.
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
    ]

    # ForeignKey para o modelo de usuário do Django.
    # on_delete=CASCADE: se o usuário for deletado, seus pedidos também são deletados.
    # Faz sentido aqui pois pedido sem cliente não tem utilidade.
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')

    criado_em = models.DateTimeField(auto_now_add=True)

    # choices=STATUS_CHOICES restringe os valores aceitos para os definidos acima.
    # default='pendente': todo pedido começa como pendente.
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        # f-string com self.pk (chave primária = id gerado automaticamente)
        return f'Pedido #{self.pk} - {self.cliente.username} ({self.status})'


# =============================================================================
# ITEM DE PEDIDO
# =============================================================================

class ItemPedido(models.Model):
    """
    Tabela intermediária entre Pedido e Produto.
    Cada linha representa "X unidades do produto Y no pedido Z".

    Por que guardar preco_unitario aqui?
    Porque o preço do produto pode mudar depois da compra.
    Guardamos o preço NO MOMENTO da compra para garantir integridade histórica.
    """

    # Ao deletar o pedido, seus itens são deletados junto (CASCADE).
    # related_name='itens' permite acessar com: pedido.itens.all()
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')

    # Ao deletar o produto, o que fazer? CASCADE deletaria o histórico de compras.
    # Na prática você usaria PROTECT ou SET_NULL, mas aqui CASCADE está OK para o exercício.
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

    # PositiveIntegerField garante que quantidade nunca seja negativa ou zero.
    quantidade = models.PositiveIntegerField(default=1)

    # Preço no momento da compra — independente do preço atual do produto.
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'
