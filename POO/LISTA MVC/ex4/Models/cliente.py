from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from Models.base import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)

    pedidos = relationship("Pedido", back_populates="cliente")

    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome!r})"
