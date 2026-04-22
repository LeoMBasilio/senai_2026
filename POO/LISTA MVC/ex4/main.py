'''Exercício 4 – Relacionamento 1:N
Modelos Cliente e Pedido. Um cliente tem vários pedidos. Listar pedidos por cliente.'''

from Controllers.loja_controller import inicializar, inserir_cliente, inserir_pedido, listar_pedidos_por_cliente
from Views.loja_view import exibir_cliente_criado, exibir_pedido_criado, exibir_pedidos_por_cliente

inicializar()

# Cria dois clientes para demonstrar que os pedidos ficam isolados por cliente.
c1 = inserir_cliente("Ana Lima", "ana@email.com")
c2 = inserir_cliente("Pedro Souza", "pedro@email.com")
exibir_cliente_criado(c1)
exibir_cliente_criado(c2)

# Três pedidos para c1 e um para c2 — confirma que a listagem filtra corretamente.
pedidos = [
    ("Notebook Dell", c1.id),
    ("Mouse Gamer", c1.id),
    ("Teclado Mecânico", c1.id),
    ("Monitor 24\"", c2.id),
]

for descricao, cliente_id in pedidos:
    p = inserir_pedido(descricao, cliente_id)
    exibir_pedido_criado(p)

# Exibe pedidos separados por cliente para provar o relacionamento 1:N.
cliente, pedidos_ana = listar_pedidos_por_cliente(c1.id)
exibir_pedidos_por_cliente(cliente, pedidos_ana)

cliente, pedidos_pedro = listar_pedidos_por_cliente(c2.id)
exibir_pedidos_por_cliente(cliente, pedidos_pedro)
