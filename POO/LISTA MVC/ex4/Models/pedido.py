from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from Models.base import Base


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(200), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="pedidos")

    def __repr__(self):
        return f"Pedido(id={self.id}, descricao={self.descricao!r}, cliente_id={self.cliente_id})"
