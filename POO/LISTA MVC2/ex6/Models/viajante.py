# Models/viajante.py — representa o agente que viaja no tempo
# ano_base é o ponto de partida do viajante — o "presente" dele.

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Models.base import Base


class Viajante(Base):
    __tablename__ = "viajantes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    ano_base = Column(Integer, nullable=False, default=2025)  # ano de origem do viajante

    # Um viajante pode fazer várias viagens ao longo da narrativa (1:N com Viagem).
    viagens = relationship("Viagem", back_populates="viajante")

    def __repr__(self):
        return f"Viajante(id={self.id}, nome={self.nome!r}, ano_base={self.ano_base})"
