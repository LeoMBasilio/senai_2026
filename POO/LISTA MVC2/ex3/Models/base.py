# Models/base.py — configuração de banco do ex3 (gerenciador de tarefas)

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tarefas.db")


class Base(DeclarativeBase):
    pass


def banco():
    return create_engine(f"sqlite:///{DB_PATH}", echo=False)


def session():
    return sessionmaker(bind=banco())()
