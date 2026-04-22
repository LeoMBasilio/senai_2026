'''Exercício 5 – Relacionamento com Mais Dados
Pedido, ItemPedido e Produto. Calcular total do pedido.'''

from Controllers.pedido_controller import inicializar, inserir_produto, criar_pedido
from Views.pedido_view import exibir_produto_criado, exibir_pedido

inicializar()

# Cria produtos com preços conhecidos para facilitar verificação manual do total.
p1 = inserir_produto("Notebook", 3500.00)
p2 = inserir_produto("Mouse", 89.90)
p3 = inserir_produto("Teclado", 150.00)
for p in [p1, p2, p3]:
    exibir_produto_criado(p)

# Pedido 1: 1 Notebook + 2 Mouses → 3500 + 179.80 = R$3679.80
pedido, itens, total = criar_pedido([(p1.id, 1), (p2.id, 2)])
exibir_pedido(pedido, itens, total)

# Pedido 2: 3 Mouses + 1 Teclado → 269.70 + 150.00 = R$419.70
pedido2, itens2, total2 = criar_pedido([(p2.id, 3), (p3.id, 1)])
exibir_pedido(pedido2, itens2, total2)
