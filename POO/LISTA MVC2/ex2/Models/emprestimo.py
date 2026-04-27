from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from Models.base import Base


class Emprestimo(Base):
    __tablename__ = "emprestimos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    livro_id = Column(Integer, ForeignKey("livros.id"), nullable=False)
    data_emprestimo = Column(DateTime, default=datetime.now, nullable=False)
    data_devolucao = Column(DateTime, nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)

    usuario = relationship("Usuario", back_populates="emprestimos")
    livro = relationship("Livro", back_populates="emprestimos")

    def __repr__(self):
        return (
            f"Emprestimo(id={self.id}, livro={self.livro_id}, "
            f"usuario={self.usuario_id}, ativo={self.ativo})"
        )
