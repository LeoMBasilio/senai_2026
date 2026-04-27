# Models/viagem.py — registra uma viagem no tempo feita por um viajante
# Cada viagem aponta para o evento que foi alterado e descreve a mudança.
# Após a viagem, uma nova linha do tempo é criada (referenciada em linhas_geradas).

from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from Models.base import Base


class Viagem(Base):
    __tablename__ = "viagens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    viajante_id = Column(Integer, ForeignKey("viajantes.id"), nullable=False)
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)  # evento alterado
    ano_destino = Column(Integer, nullable=False)   # ano para o qual o viajante foi
    alteracao = Column(Text, nullable=False)        # descrição da mudança feita no evento
    realizada_em = Column(DateTime, default=datetime.now)

    viajante = relationship("Viajante", back_populates="viagens")

    # Uma viagem pode gerar várias linhas do tempo (normalmente uma, mas o modelo permite mais).
    # foreign_keys="LinhaTempo.origem_viagem_id" resolve a ambiguidade de FK como string.
    linhas_geradas = relationship(
        "LinhaTempo",
        back_populates="origem_viagem",
        foreign_keys="LinhaTempo.origem_viagem_id",
    )

    def __repr__(self):
        return f"Viagem(viajante={self.viajante_id}, ano={self.ano_destino}, alteracao={self.alteracao!r})"
