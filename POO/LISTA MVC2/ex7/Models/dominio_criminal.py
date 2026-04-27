# Models/dominio_criminal.py — representa o território controlado por um vilão
# unique=True em vilao_id garante relação 1:1 — cada vilão tem exatamente um domínio.
# pontos_dominio crescem a cada crime bem-sucedido e ao conquistar território.

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from Models.base import Base


class DominioCriminal(Base):
    __tablename__ = "dominios"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # unique=True: garante que um vilão não possa ter dois domínios (relação 1:1).
    vilao_id = Column(Integer, ForeignKey("viloes.id"), unique=True, nullable=False)
    territorio = Column(String(200), default="Esconderijo Secreto")  # local inicial
    pontos_dominio = Column(Float, default=0.0)  # medida da extensão do domínio

    vilao = relationship("Vilao", back_populates="dominio")

    def __repr__(self):
        return f"Dominio(vilao={self.vilao_id}, territorio={self.territorio!r}, pontos={self.pontos_dominio})"
