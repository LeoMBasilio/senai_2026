# Models/usuario.py — representa o leitor da biblioteca
# relationship("Emprestimo"): um usuário pode ter VÁRIOS empréstimos (relação 1:N).
# back_populates="usuario" conecta o lado N (Emprestimo.usuario) de volta a este lado.

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Models.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)

    # Lado "1" da relação 1:N — um usuário possui muitos empréstimos.
    emprestimos = relationship("Emprestimo", back_populates="usuario")

    def __repr__(self):
        return f"Usuario(id={self.id}, nome={self.nome!r})"
