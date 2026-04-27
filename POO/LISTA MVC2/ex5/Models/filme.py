# Models/filme.py — representa um filme do catálogo
# genero e diretor são opcionais (nullable=True) — permitindo cadastros parciais.

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Models.base import Base


class Filme(Base):
    __tablename__ = "filmes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    ano = Column(Integer, nullable=False)
    genero = Column(String(100), nullable=True)   # campo opcional
    diretor = Column(String(150), nullable=True)  # campo opcional

    # Um filme pode receber várias avaliações (1:N com Avaliacao).
    avaliacoes = relationship("Avaliacao", back_populates="filme")

    def __repr__(self):
        return f"Filme(id={self.id}, titulo={self.titulo!r}, ano={self.ano})"
