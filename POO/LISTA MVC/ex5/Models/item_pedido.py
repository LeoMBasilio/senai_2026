from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from Models.base import Base


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)

    # preco_unitario é armazenado no item — não no produto — porque o preço do produto
    # pode mudar no futuro. O item "congela" o preço no momento da compra.
    preco_unitario = Column(Float, nullable=False)

    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto")  # sem back_populates: Produto não precisa saber dos itens

    def __repr__(self):
        return f"ItemPedido(produto_id={self.produto_id}, qty={self.quantidade}, unit={self.preco_unitario})"
