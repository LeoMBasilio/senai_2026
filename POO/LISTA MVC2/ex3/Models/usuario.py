# Models/usuario.py — representa o responsável pelas tarefas
# Um usuário pode ter várias tarefas (relação 1:N com Tarefa).

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Models.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    # Lado "1" da relação: um usuário possui muitas tarefas.
    tarefas = relationship("Tarefa", back_populates="usuario")

    def __repr__(self):
        return f"Usuario(id={self.id}, nome={self.nome!r})"
