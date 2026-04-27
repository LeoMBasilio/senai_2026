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

p1 = cadastrar_produto("Teclado Mecanico", 350.00, 10)
p2 = cadastrar_produto("Mouse Gamer", 180.50, 5)
p3 = cadastrar_produto('Monitor 24"', 1299.90, 3)
p4 = cadastrar_produto("Headset USB", 220.00, 8)

exibir_catalogo(listar_produtos())

lucas = cadastrar_usuario("Lucas Ferreira", "lucas@email.com")

pedido1 = abrir_pedido(lucas.id)
adicionar_item(pedido1.id, p1.id, 1)
adicionar_item(pedido1.id, p2.id, 2)
print(f"\n  Itens adicionados ao pedido #{pedido1.id}.")

try:
    adicionar_item(pedido1.id, p3.id, 10)
except ValueError as e:
    print(f"  [ESTOQUE] {e}")

confirmar_pedido(pedido1.id)

pedido2 = abrir_pedido(lucas.id)
adicionar_item(pedido2.id, p4.id, 3)
cancelar_pedido(pedido2.id)
print(f"\n  Pedido #{pedido2.id} cancelado — estoque do headset restaurado.")

exibir_catalogo(listar_produtos())
exibir_pedidos(listar_pedidos_usuario(lucas.id), f"Pedidos de {lucas.nome}")
