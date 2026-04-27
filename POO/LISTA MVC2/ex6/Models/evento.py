from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from Models.base import Base


class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(300), nullable=False)
    ano = Column(Integer, nullable=False)
    alterado = Column(Boolean, default=False)
    descricao_original = Column(String(300), nullable=True)
    linha_tempo_id = Column(Integer, ForeignKey("linhas_tempo.id"), nullable=False)

    linha_tempo = relationship("LinhaTempo", back_populates="eventos")

    def __repr__(self):
        tag = " [ALTERADO]" if self.alterado else ""
        return f"Evento(ano={self.ano}, desc={self.descricao!r}{tag})"
