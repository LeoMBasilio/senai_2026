from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from Models.base import Base
from Models.associacoes import aluno_curso


class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    # O mesmo secondary é usado nos dois lados — ambos enxergam a mesma tabela de junção.
    alunos = relationship("Aluno", secondary=aluno_curso, back_populates="cursos")

    def __repr__(self):
        return f"Curso(id={self.id}, nome={self.nome!r})"
