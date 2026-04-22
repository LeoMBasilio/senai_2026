from sqlalchemy import Column, Integer, ForeignKey, Table

from Models.base import Base

# Tabela associativa N:N entre Aluno e Curso.
# Usa Table() em vez de uma classe completa pois não tem atributos extras.
aluno_curso = Table(
    "aluno_curso",
    Base.metadata,
    Column("aluno_id", Integer, ForeignKey("alunos.id"), primary_key=True),
    Column("curso_id", Integer, ForeignKey("cursos.id"), primary_key=True),
)
