# models.py — Define a estrutura das tabelas no banco de dados.
# Cada classe que herda de models.Model vira uma tabela no SQLite.
# O Django cria as colunas automaticamente a partir dos campos definidos aqui.

from django.db import models


class Categoria(models.Model):
    # CharField armazena texto curto (VARCHAR no banco).
    # max_length=100 define o tamanho máximo.
    # unique=True garante que não existam duas categorias com o mesmo nome.
    nome = models.CharField(max_length=100, unique=True)

    # TextField armazena texto longo (TEXT no banco), sem limite de tamanho.
    # blank=True permite enviar esse campo vazio nos formulários e na API.
    descricao = models.TextField(blank=True)

    # BooleanField armazena True ou False (1 ou 0 no banco).
    # default=True significa que toda categoria criada começa como ativa
    # sem precisar informar o campo explicitamente.
    ativa = models.BooleanField(default=True)

    def __str__(self):
        # __str__ define o que aparece quando imprimimos o objeto,
        # por exemplo no admin do Django e no shell.
        return self.nome

    class Meta:
        # Meta configura comportamentos extras do model.
        # verbose_name e verbose_name_plural ajustam os rótulos no admin.
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


class Produto(models.Model):
    nome = models.CharField(max_length=200)

    descricao = models.TextField(blank=True)

    # DecimalField armazena números com casas decimais de forma precisa.
    # Ideal para dinheiro — float pode ter erros de arredondamento.
    # max_digits=10: no máximo 10 dígitos no total.
    # decimal_places=2: sempre 2 casas decimais (ex: 3500.00).
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    # IntegerField armazena números inteiros.
    # default=0: se não informar o estoque, começa em zero.
    estoque = models.IntegerField(default=0)

    ativo = models.BooleanField(default=True)

    # DateTimeField armazena data e hora.
    # auto_now_add=True preenche automaticamente com a data/hora atual
    # no momento da criação — o campo fica imutável depois disso.
    criado_em = models.DateTimeField(auto_now_add=True)

    # ForeignKey cria o relacionamento "muitos para um":
    # muitos produtos podem pertencer a uma categoria.
    # on_delete=SET_NULL: se a categoria for deletada, o campo vira NULL
    # em vez de deletar o produto junto — protege os dados.
    # null=True: permite valor NULL no banco (coluna aceita vazio).
    # blank=True: permite enviar vazio pela API/formulário.
    # related_name='produtos': permite acessar todos os produtos de uma
    # categoria com categoria.produtos.all()
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produtos',
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
