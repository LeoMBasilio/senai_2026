from sqlalchemy import Column, Integer, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from Models.base import Base
from Models.status_pedido import StatusPedido


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    status = Column(Enum(StatusPedido), default=StatusPedido.ABERTO, nullable=False)
    total = Column(Float, default=0.0, nullable=False)
    criado_em = Column(DateTime, default=datetime.now)

    usuario = relationship("Usuario", back_populates="pedidos")
    itens = relationship("ItemPedido", back_populates="pedido")

    def __repr__(self):
        return f"Pedido(id={self.id}, usuario={self.usuario_id}, total=R${self.total:.2f}, status={self.status.value})"
