from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Models.base import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)
    descricao = Column(String(255), nullable=True)

    tarefas = relationship("Tarefa", back_populates="categoria")

    def __repr__(self):
        return f"Categoria(id={self.id}, nome={self.nome!r})"
