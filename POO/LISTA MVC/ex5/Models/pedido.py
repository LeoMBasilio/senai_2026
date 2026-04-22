from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from Models.base import Base


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Um pedido possui vários itens — 1:N entre Pedido e ItemPedido.
    itens = relationship("ItemPedido", back_populates="pedido")

    def __repr__(self):
        return f"Pedido(id={self.id})"
