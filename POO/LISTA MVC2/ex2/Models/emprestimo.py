# Models/emprestimo.py — registra cada empréstimo de livro
# É a tabela de relacionamento entre Usuario e Livro, com dados extras (datas, status).
# Diferente de uma tabela N:N pura, Emprestimo tem atributos próprios — por isso é uma classe.

from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from Models.base import Base


class Emprestimo(Base):
    __tablename__ = "emprestimos"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # ForeignKey cria a FK para as tabelas relacionadas — garante integridade referencial.
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    livro_id = Column(Integer, ForeignKey("livros.id"), nullable=False)

    # default=datetime.now: grava a data/hora atual automaticamente ao criar o empréstimo.
    data_emprestimo = Column(DateTime, default=datetime.now, nullable=False)

    # nullable=True: data_devolucao fica vazia até o livro ser devolvido.
    data_devolucao = Column(DateTime, nullable=True)

    # ativo=True indica que o empréstimo ainda está em curso.
    # Ao devolver, ativo vira False e data_devolucao é preenchida.
    ativo = Column(Boolean, default=True, nullable=False)

    # Lado "N" das relações — cada empréstimo pertence a um usuário e um livro.
    usuario = relationship("Usuario", back_populates="emprestimos")
    livro = relationship("Livro", back_populates="emprestimos")

    def __repr__(self):
        return (
            f"Emprestimo(id={self.id}, livro={self.livro_id}, "
            f"usuario={self.usuario_id}, ativo={self.ativo})"
        )
