# ============================================================
# models.py — Define a estrutura dos dados da aplicação
#
# Um "Model" representa uma tabela no banco de dados.
# Cada atributo da classe vira uma coluna nessa tabela.
# O Django cuida de criar e gerenciar a tabela automaticamente.
# ============================================================

from django.db import models  # importa a base para criar modelos


# Criamos uma classe que herda de models.Model.
# Isso diz ao Django: "essa classe é uma tabela no banco de dados".
class Produto(models.Model):

    # CharField → coluna de texto curto (equivale a VARCHAR no SQL)
    # max_length=200 → limite de 200 caracteres
    nome = models.CharField(max_length=200)

    # TextField → texto longo, sem limite fixo (equivale a TEXT no SQL)
    # blank=True → o campo pode ser enviado vazio no formulário/API
    descricao = models.TextField(blank=True)

    # DecimalField → número com casas decimais (ideal para dinheiro)
    # max_digits=10  → no máximo 10 dígitos no total (ex: 99999999.99)
    # decimal_places=2 → sempre 2 casas decimais (ex: 19.90)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    # IntegerField → número inteiro (sem casas decimais)
    # default=0 → se não informado, começa com zero
    estoque = models.IntegerField(default=0)

    # BooleanField → verdadeiro ou falso (True/False)
    # default=True → todo produto começa como ativo
    ativo = models.BooleanField(default=True)

    # DateTimeField → data e hora
    # auto_now_add=True → preenchido AUTOMATICAMENTE com a data/hora
    #                      de criação; não pode ser alterado depois
    criado_em = models.DateTimeField(auto_now_add=True)

    # __str__ define o que aparece quando imprimimos um objeto Produto.
    # Sem isso, apareceria algo como <Produto object (1)>.
    def __str__(self):
        return self.nome  # exibe o nome do produto no lugar
