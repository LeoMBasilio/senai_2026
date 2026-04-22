'''Exercício 2 – Encapsulamento com Regra
Modelo Produto com id, nome, preco, estoque. Não permitir valores negativos.
Métodos para atualizar.'''

# main.py é o ponto de entrada da aplicação.
# Ele apenas coordena chamadas entre Controller e View — não contém lógica de negócio.

from Controllers.produto_controller import inicializar, inserir_produto, atualizar_preco, atualizar_estoque, listar_produtos
from Views.produto_view import exibir_produto_criado, exibir_produto_atualizado, exibir_lista, exibir_erro

# Garante que a tabela existe antes de qualquer operação.
inicializar()

produtos_novos = [
    ("Notebook", 3500.00, 10),
    ("Mouse", 89.90, 50),
    ("Teclado", 150.00, 30),
]

criados = []
for nome, preco, estoque in produtos_novos:
    p = inserir_produto(nome, preco, estoque)
    exibir_produto_criado(p)
    criados.append(p)  # guarda referência para usar os ids nas operações abaixo

exibir_lista(listar_produtos())

# Demonstra atualização de preço e estoque passando pelos setters com validação.
p = atualizar_preco(criados[0].id, 3200.00)
exibir_produto_atualizado(p)

p = atualizar_estoque(criados[1].id, 45)
exibir_produto_atualizado(p)

# Demonstra que as regras de encapsulamento realmente bloqueiam valores inválidos.
print("\n[Testando validação de valor negativo]")
try:
    inserir_produto("Invalido", -10.0, 5)
except ValueError as e:
    exibir_erro(str(e))

try:
    atualizar_estoque(criados[0].id, -1)
except ValueError as e:
    exibir_erro(str(e))
