# Models/tarefa.py — representa uma tarefa do sistema
# Tem duas FKs: pertence a um Usuario e a uma Categoria.
# O status usa Enum para restringir os valores aceitos.

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from Models.base import Base
from Models.status_tarefa import StatusTarefa


class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    descricao = Column(String(500), nullable=True)  # campo opcional

    # Enum(StatusTarefa): o SQLAlchemy valida que o valor é um membro da enumeração.
    # default=StatusTarefa.PENDENTE: toda tarefa começa como pendente.
    status = Column(Enum(StatusTarefa), default=StatusTarefa.PENDENTE, nullable=False)

    # datetime.now (sem parênteses): passa a função, não o resultado.
    # Assim cada tarefa grava a data/hora no momento em que é criada, não ao definir a classe.
    criada_em = Column(DateTime, default=datetime.now)

    # onupdate=datetime.now: atualiza este campo automaticamente a cada commit de mudança.
    atualizada_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # FKs obrigatórias: toda tarefa deve ter um dono e uma categoria.
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="tarefas")
    categoria = relationship("Categoria", back_populates="tarefas")

    def __repr__(self):
        # .value acessa a string do Enum (ex: "pendente") em vez do nome Python (PENDENTE).
        return f"Tarefa(id={self.id}, titulo={self.titulo!r}, status={self.status.value})"
