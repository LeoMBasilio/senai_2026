from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Models.base import Base
import Models.aluno  # noqa: F401 — registra Aluno no metadata do Base
import Models.curso  # noqa: F401 — registra Curso no metadata do Base

ENGINE = create_engine("sqlite:///escola.db", echo=False)


def criar_tabelas():
    Base.metadata.create_all(ENGINE)


def get_session():
    return sessionmaker(bind=ENGINE)()
