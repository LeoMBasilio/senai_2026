from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from Models.base import Base


class LinhaTempo(Base):
    __tablename__ = "linhas_tempo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    descricao = Column(Text, nullable=True)
    original = Column(Boolean, default=False)
    criada_em = Column(DateTime, default=datetime.now)
    origem_viagem_id = Column(Integer, ForeignKey("viagens.id"), nullable=True)

    eventos = relationship("Evento", back_populates="linha_tempo")
    origem_viagem = relationship(
        "Viagem",
        back_populates="linhas_geradas",
        foreign_keys=[origem_viagem_id],
    )

    def __repr__(self):
        tag = " [ORIGINAL]" if self.original else ""
        return f"LinhaTempo(id={self.id}, nome={self.nome!r}{tag})"
