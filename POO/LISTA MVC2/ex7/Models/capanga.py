from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Models.base import Base


class Capanga(Base):
    __tablename__ = "capangas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    habilidade = Column(String(100), nullable=False)
    lealdade = Column(Integer, default=100)
    vilao_id = Column(Integer, ForeignKey("viloes.id"), nullable=False)

    vilao = relationship("Vilao", back_populates="capangas")

    def __repr__(self):
        return f"Capanga(id={self.id}, nome={self.nome!r}, habilidade={self.habilidade!r})"
