from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Models.base import Base


class Filme(Base):
    __tablename__ = "filmes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    ano = Column(Integer, nullable=False)
    genero = Column(String(100), nullable=True)
    diretor = Column(String(150), nullable=True)

    avaliacoes = relationship("Avaliacao", back_populates="filme")

    def __repr__(self):
        return f"Filme(id={self.id}, titulo={self.titulo!r}, ano={self.ano})"
