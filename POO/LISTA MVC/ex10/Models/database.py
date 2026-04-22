from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Models.base import Base
import Models.usuario  # noqa: F401 — registra Usuario no metadata do Base
import Models.tarefa   # noqa: F401 — registra Tarefa no metadata do Base

ENGINE = create_engine("sqlite:///tarefas.db", echo=False)


def criar_tabelas():
    Base.metadata.create_all(ENGINE)


def get_session():
    return sessionmaker(bind=ENGINE)()
