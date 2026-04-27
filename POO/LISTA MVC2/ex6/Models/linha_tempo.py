# Models/linha_tempo.py — representa uma linha do tempo (universo paralelo)
# Quando um viajante altera um evento, uma nova LinhaTempo divergente é criada.
# A linha original tem original=True; as criadas por viagens têm original=False.
# origem_viagem_id aponta para a Viagem que gerou esta divergência.

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from Models.base import Base


class LinhaTempo(Base):
    __tablename__ = "linhas_tempo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    descricao = Column(Text, nullable=True)
    original = Column(Boolean, default=False)  # True apenas para a linha primordial
    criada_em = Column(DateTime, default=datetime.now)

    # FK opcional: linhas originais não têm origem_viagem_id (nullable=True).
    # Linhas divergentes apontam para a viagem que as criou.
    origem_viagem_id = Column(Integer, ForeignKey("viagens.id"), nullable=True)

    eventos = relationship("Evento", back_populates="linha_tempo")

    # foreign_keys especifica qual FK usar quando há múltiplas FKs para a mesma tabela.
    origem_viagem = relationship(
        "Viagem",
        back_populates="linhas_geradas",
        foreign_keys=[origem_viagem_id],
    )

    def __repr__(self):
        tag = " [ORIGINAL]" if self.original else ""
        return f"LinhaTempo(id={self.id}, nome={self.nome!r}{tag})"
