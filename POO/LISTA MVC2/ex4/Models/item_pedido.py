# Models/item_pedido.py — representa cada produto dentro de um pedido
# Armazena o preco_unitario no momento da compra — assim o preço do produto pode mudar
# no futuro sem alterar o valor registrado no pedido histórico.
# @property subtotal é calculado na memória, sem coluna extra no banco.

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from Models.base import Base


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)

    # Congelar o preço no item evita que uma promoção futura altere pedidos passados.
    preco_unitario = Column(Float, nullable=False)

    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="itens")

    @property
    def subtotal(self) -> float:
        # @property: acessado como item.subtotal sem parênteses — calculado na hora, sem banco.
        return self.quantidade * self.preco_unitario

    def __repr__(self):
        return f"ItemPedido(produto={self.produto_id}, qtd={self.quantidade}, subtotal=R${self.subtotal:.2f})"
