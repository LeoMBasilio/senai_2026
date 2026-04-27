# Models/categoria.py — agrupa tarefas por tema (ex: Trabalho, Pessoal, Estudo)
# unique=True na coluna nome impede categorias duplicadas.

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Models.base import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # unique=True: não pode haver duas categorias com o mesmo nome.
    nome = Column(String(100), nullable=False, unique=True)
    descricao = Column(String(255), nullable=True)  # campo opcional

    # Uma categoria pode conter muitas tarefas (1:N com Tarefa).
    tarefas = relationship("Tarefa", back_populates="categoria")

    def __repr__(self):
        return f"Categoria(id={self.id}, nome={self.nome!r})"
