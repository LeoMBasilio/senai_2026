import enum


class StatusPedido(enum.Enum):
    ABERTO = "aberto"
    CONFIRMADO = "confirmado"
    CANCELADO = "cancelado"
    ENTREGUE = "entregue"
