from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from Models.base import Base


class DominioCriminal(Base):
    __tablename__ = "dominios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vilao_id = Column(Integer, ForeignKey("viloes.id"), unique=True, nullable=False)
    territorio = Column(String(200), default="Esconderijo Secreto")
    pontos_dominio = Column(Float, default=0.0)

    vilao = relationship("Vilao", back_populates="dominio")

    def __repr__(self):
        return f"Dominio(vilao={self.vilao_id}, territorio={self.territorio!r}, pontos={self.pontos_dominio})"
