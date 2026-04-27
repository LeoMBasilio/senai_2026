# Models/pedido.py — representa um pedido de compra
# O total é calculado e acumulado no Controller a cada item adicionado.
# O status controla o ciclo de vida do pedido.

from sqlalchemy import Column, Integer, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from Models.base import Base
from Models.status_pedido import StatusPedido


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Pedido começa como ABERTO — permite adicionar itens antes de confirmar.
    status = Column(Enum(StatusPedido), default=StatusPedido.ABERTO, nullable=False)

    # total é atualizado pelo Controller a cada item adicionado.
    total = Column(Float, default=0.0, nullable=False)
    criado_em = Column(DateTime, default=datetime.now)

    usuario = relationship("Usuario", back_populates="pedidos")
    itens = relationship("ItemPedido", back_populates="pedido")

    def __repr__(self):
        return f"Pedido(id={self.id}, usuario={self.usuario_id}, total=R${self.total:.2f}, status={self.status.value})"
