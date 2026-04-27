from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from Models.base import Base


class Vilao(Base):
    __tablename__ = "viloes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    codinome = Column(String(100), nullable=True)
    poder_mundial = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)

    capangas = relationship("Capanga", back_populates="vilao")
    crimes = relationship("Crime", back_populates="vilao")
    dominio = relationship("DominioCriminal", back_populates="vilao", uselist=False)

    def __repr__(self):
        return f"Vilao(id={self.id}, nome={self.nome!r}, poder={self.poder_mundial})"
