# Models/evento.py — representa um acontecimento histórico em uma linha do tempo
# alterado=True indica que este evento foi modificado por uma viagem no tempo.
# descricao_original guarda o texto do evento antes da alteração para comparação.

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from Models.base import Base


class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(300), nullable=False)  # o que aconteceu (ou o que foi alterado)
    ano = Column(Integer, nullable=False)             # ano histórico do evento
    alterado = Column(Boolean, default=False)         # True se foi modificado por uma viagem

    # Preserva o texto original antes da alteração — permite comparar as duas versões.
    descricao_original = Column(String(300), nullable=True)

    # Todo evento pertence a uma linha do tempo específica.
    linha_tempo_id = Column(Integer, ForeignKey("linhas_tempo.id"), nullable=False)
    linha_tempo = relationship("LinhaTempo", back_populates="eventos")

    def __repr__(self):
        tag = " [ALTERADO]" if self.alterado else ""
        return f"Evento(ano={self.ano}, desc={self.descricao!r}{tag})"
