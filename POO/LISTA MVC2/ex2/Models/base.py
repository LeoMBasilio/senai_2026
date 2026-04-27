# Models/base.py — configuração de banco do ex2 (biblioteca)
# os.path garante que o caminho do banco seja absoluto, independente de onde o script é executado.

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# __file__ é o caminho deste arquivo; abspath torna-o absoluto; dirname sobe um nível (para ex2/).
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "biblioteca.db")


class Base(DeclarativeBase):
    pass


def banco():
    return create_engine(f"sqlite:///{DB_PATH}", echo=False)


def session():
    return sessionmaker(bind=banco())()
