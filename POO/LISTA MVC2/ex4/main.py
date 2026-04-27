"""Loja: visualizacao de produtos, compras e gerenciamento de estoque."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

_db = os.path.join(os.path.dirname(__file__), "loja.db")
if os.path.exists(_db):
    os.remove(_db)

from Controllers.loja_controller import (
    inicializar, cadastrar_usuario, cadastrar_produto, listar_produtos,
    abrir_pedido, adicionar_item, confirmar_pedido, cancelar_pedido,
    listar_pedidos_usuario,
)
from Views.loja_view import exibir_catalogo, exibir_pedidos

inicializar()

# Cadastra quatro produtos com estoques variados para testar a verificação de estoque.
p1 = cadastrar_produto("Teclado Mecanico", 350.00, 10)
p2 = cadastrar_produto("Mouse Gamer", 180.50, 5)
p3 = cadastrar_produto('Monitor 24"', 1299.90, 3)
p4 = cadastrar_produto("Headset USB", 220.00, 8)

# Exibe o catálogo inicial — todos os produtos com estoque cheio.
exibir_catalogo(listar_produtos())

lucas = cadastrar_usuario("Lucas Ferreira", "lucas@email.com")

# Pedido 1: abre, adiciona 2 itens e confirma.
pedido1 = abrir_pedido(lucas.id)
adicionar_item(pedido1.id, p1.id, 1)  # 1 teclado — estoque cai de 10 para 9
adicionar_item(pedido1.id, p2.id, 2)  # 2 mouses — estoque cai de 5 para 3
print(f"\n  Itens adicionados ao pedido #{pedido1.id}.")

# Testa a regra de estoque insuficiente: pede 10 monitores mas só há 3.
try:
    adicionar_item(pedido1.id, p3.id, 10)
except ValueError as e:
    print(f"  [ESTOQUE] {e}")

confirmar_pedido(pedido1.id)  # muda status para CONFIRMADO

# Pedido 2: abre, adiciona 3 headsets e cancela — o estoque deve ser restaurado.
pedido2 = abrir_pedido(lucas.id)
adicionar_item(pedido2.id, p4.id, 3)  # estoque de headset: 8 → 5
cancelar_pedido(pedido2.id)           # estoque de headset: 5 → 8 (devolvido)
print(f"\n  Pedido #{pedido2.id} cancelado — estoque do headset restaurado.")

# O catálogo deve refletir o estoque após os pedidos (teclado -1, mouse -2, resto igual).
exibir_catalogo(listar_produtos())

# Lista todos os pedidos de Lucas com seus itens e status.
exibir_pedidos(listar_pedidos_usuario(lucas.id), f"Pedidos de {lucas.nome}")
