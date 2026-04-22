from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from Models.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)

    # cascade="all, delete-orphan": quando o usuário for deletado,
    # todas as suas tarefas são deletadas junto (DELETE em cascata).
    tarefas = relationship("Tarefa", back_populates="usuario", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Usuario(id={self.id}, nome={self.nome!r}, email={self.email!r})"
