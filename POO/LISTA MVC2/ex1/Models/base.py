# Models/base.py — configuração de banco do ex1 (mini-RPG)
# Centraliza o engine e a session para que todas as Models usem a mesma conexão.
# Separar aqui evita criar vários engines apontando para o mesmo arquivo de banco.

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Base é a classe-pai de todos os modelos ORM deste exercício.
# Toda classe que herdar de Base terá sua tabela gerenciada pelo SQLAlchemy.
class Base(DeclarativeBase):
    pass


def banco():
    # Cria (ou reutiliza) o arquivo rpg.db na pasta atual.
    # echo=False suprime o log de SQL no terminal — útil para manter o output limpo.
    return create_engine("sqlite:///rpg.db", echo=False)


def session():
    # sessionmaker retorna uma fábrica; () no final cria e retorna a sessão aberta.
    return sessionmaker(bind=banco())()
