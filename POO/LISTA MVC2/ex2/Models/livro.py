# Models/livro.py — representa um livro no acervo da biblioteca
# O campo "disponivel" é a regra central do sistema: controla se o livro pode ser emprestado.
# Quando alguém pega emprestado, disponivel vira False; ao devolver, volta para True.

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from Models.base import Base


class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(150), nullable=False)

    # default=True: todo livro começa disponível ao ser cadastrado.
    disponivel = Column(Boolean, default=True, nullable=False)

    # Lado "1" da relação 1:N com Emprestimo.
    emprestimos = relationship("Emprestimo", back_populates="livro")

    def __repr__(self):
        status = "disponivel" if self.disponivel else "emprestado"
        return f"Livro(id={self.id}, titulo={self.titulo!r}, status={status})"
