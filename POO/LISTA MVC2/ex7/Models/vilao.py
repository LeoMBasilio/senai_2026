# Models/vilao.py — representa um vilão e seu poder acumulado
# poder_mundial aumenta a cada crime bem-sucedido e diminui a cada falha.
# uselist=False em dominio indica relação 1:1 — um vilão tem exatamente um domínio.

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from Models.base import Base


class Vilao(Base):
    __tablename__ = "viloes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    codinome = Column(String(100), nullable=True)   # apelido opcional (ex: "Joker")
    poder_mundial = Column(Integer, default=0)      # pontuação acumulada de poder
    ativo = Column(Boolean, default=True)           # False quando o vilão é derrotado

    # 1:N com Capanga — um vilão pode ter vários capangas.
    capangas = relationship("Capanga", back_populates="vilao")

    # 1:N com Crime — um vilão planeja e executa vários crimes.
    crimes = relationship("Crime", back_populates="vilao")

    # 1:1 com DominioCriminal — uselist=False: retorna um objeto, não uma lista.
    dominio = relationship("DominioCriminal", back_populates="vilao", uselist=False)

    def __repr__(self):
        return f"Vilao(id={self.id}, nome={self.nome!r}, poder={self.poder_mundial})"
