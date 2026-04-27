from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from Models.base import Base
from Models.status_tarefa import StatusTarefa


class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    descricao = Column(String(500), nullable=True)
    status = Column(Enum(StatusTarefa), default=StatusTarefa.PENDENTE, nullable=False)
    criada_em = Column(DateTime, default=datetime.now)
    atualizada_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="tarefas")
    categoria = relationship("Categoria", back_populates="tarefas")

    def __repr__(self):
        return f"Tarefa(id={self.id}, titulo={self.titulo!r}, status={self.status.value})"
