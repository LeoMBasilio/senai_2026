# Models/status_pedido.py — define o ciclo de vida de um pedido usando Enum
# Fluxo normal:  ABERTO → CONFIRMADO → ENTREGUE
# Fluxo de cancelamento: ABERTO ou CONFIRMADO → CANCELADO
# O Enum impede que strings inválidas entrem no banco.

import enum


class StatusPedido(enum.Enum):
    ABERTO = "aberto"          # pedido criado mas sem itens confirmados
    CONFIRMADO = "confirmado"  # cliente finalizou a compra
    CANCELADO = "cancelado"    # pedido cancelado (estoque é devolvido)
    ENTREGUE = "entregue"      # mercadoria entregue ao cliente
