# Models/crime.py — representa um crime planejado por um vilão
# recompensa_poder define quanto poder o vilão ganha se o crime for bem-sucedido
# (ou perde metade disso em caso de falha).

from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from Models.base import Base
from Models.status_crime import StatusCrime


class Crime(Base):
    __tablename__ = "crimes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=True)              # detalhes opcionais do plano
    recompensa_poder = Column(Integer, default=10)       # poder ganho em caso de sucesso
    status = Column(Enum(StatusCrime), default=StatusCrime.PLANEJADO, nullable=False)
    planejado_em = Column(DateTime, default=datetime.now)
    executado_em = Column(DateTime, nullable=True)       # preenchido ao executar

    vilao_id = Column(Integer, ForeignKey("viloes.id"), nullable=False)
    vilao = relationship("Vilao", back_populates="crimes")

    def __repr__(self):
        return f"Crime(id={self.id}, nome={self.nome!r}, status={self.status.value})"
