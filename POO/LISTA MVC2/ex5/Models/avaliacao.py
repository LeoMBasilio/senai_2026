# Models/avaliacao.py — representa uma avaliação de um usuário para um filme
# CheckConstraint valida no banco que a nota esteja entre 0 e 10.
# Embora o Controller também valide, a constraint no banco é uma segunda barreira de segurança.

from sqlalchemy import Column, Integer, Float, Text, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from Models.base import Base


class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filme_id = Column(Integer, ForeignKey("filmes.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nota = Column(Float, nullable=False)           # valor entre 0.0 e 10.0
    comentario = Column(Text, nullable=True)       # campo opcional — avaliação pode ser só nota
    criada_em = Column(DateTime, default=datetime.now)

    # __table_args__ permite passar restrições de tabela fora das colunas.
    # CheckConstraint é executado pelo banco antes de inserir/atualizar — proteção extra.
    __table_args__ = (
        CheckConstraint("nota >= 0 AND nota <= 10", name="nota_valida"),
    )

    filme = relationship("Filme", back_populates="avaliacoes")
    usuario = relationship("Usuario", back_populates="avaliacoes")

    def __repr__(self):
        return f"Avaliacao(filme={self.filme_id}, usuario={self.usuario_id}, nota={self.nota})"
