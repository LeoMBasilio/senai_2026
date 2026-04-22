from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from Models.base import Base


class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)

    # Boolean com default=False: toda tarefa começa como pendente.
    concluida = Column(Boolean, default=False, nullable=False)

    # FK obrigatória — uma tarefa sempre pertence a um usuário.
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="tarefas")

    def __repr__(self):
        status = "✓" if self.concluida else "○"
        return f"Tarefa(id={self.id}, titulo={self.titulo!r}, status={status})"
