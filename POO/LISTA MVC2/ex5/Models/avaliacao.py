from sqlalchemy import Column, Integer, Float, Text, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from Models.base import Base


class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filme_id = Column(Integer, ForeignKey("filmes.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nota = Column(Float, nullable=False)
    comentario = Column(Text, nullable=True)
    criada_em = Column(DateTime, default=datetime.now)

    __table_args__ = (
        CheckConstraint("nota >= 0 AND nota <= 10", name="nota_valida"),
    )

    filme = relationship("Filme", back_populates="avaliacoes")
    usuario = relationship("Usuario", back_populates="avaliacoes")

    def __repr__(self):
        return f"Avaliacao(filme={self.filme_id}, usuario={self.usuario_id}, nota={self.nota})"
