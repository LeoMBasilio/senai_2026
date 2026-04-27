from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from Models.base import Base


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)

    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="itens")

    @property
    def subtotal(self) -> float:
        return self.quantidade * self.preco_unitario

    def __repr__(self):
        return f"ItemPedido(produto={self.produto_id}, qtd={self.quantidade}, subtotal=R${self.subtotal:.2f})"
