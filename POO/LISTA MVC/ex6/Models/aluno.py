from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from Models.base import Base
from Models.associacoes import aluno_curso


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    # secondary aponta para a tabela de junção — o SQLAlchemy cuida dos INSERTs
    # nela automaticamente ao fazer aluno.cursos.append(curso).
    cursos = relationship("Curso", secondary=aluno_curso, back_populates="alunos")

    def __repr__(self):
        return f"Aluno(id={self.id}, nome={self.nome!r})"
