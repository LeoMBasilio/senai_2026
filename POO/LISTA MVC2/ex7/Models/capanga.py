# Models/capanga.py — representa um capanga a serviço de um vilão
# lealdade poderia ser usada futuramente para simular traições ou deserções.
# O número de capangas de um vilão influencia a chance de sucesso dos crimes.

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Models.base import Base


class Capanga(Base):
    __tablename__ = "capangas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    habilidade = Column(String(100), nullable=False)  # especialidade do capanga
    lealdade = Column(Integer, default=100)            # 0-100, quanto confia no vilão
    vilao_id = Column(Integer, ForeignKey("viloes.id"), nullable=False)

    vilao = relationship("Vilao", back_populates="capangas")

    def __repr__(self):
        return f"Capanga(id={self.id}, nome={self.nome!r}, habilidade={self.habilidade!r})"
