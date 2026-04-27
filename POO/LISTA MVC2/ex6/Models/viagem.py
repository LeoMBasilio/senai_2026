from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from Models.base import Base


class Viagem(Base):
    __tablename__ = "viagens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    viajante_id = Column(Integer, ForeignKey("viajantes.id"), nullable=False)
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    ano_destino = Column(Integer, nullable=False)
    alteracao = Column(Text, nullable=False)
    realizada_em = Column(DateTime, default=datetime.now)

    viajante = relationship("Viajante", back_populates="viagens")
    linhas_geradas = relationship(
        "LinhaTempo",
        back_populates="origem_viagem",
        foreign_keys="LinhaTempo.origem_viagem_id",
    )

    def __repr__(self):
        return f"Viagem(viajante={self.viajante_id}, ano={self.ano_destino}, alteracao={self.alteracao!r})"
