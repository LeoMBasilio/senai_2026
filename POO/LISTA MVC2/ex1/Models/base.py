import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker



class Base(DeclarativeBase):
    pass


def banco():
    return create_engine(f"sqlite:///rpg.db", echo=False)


def session():
    return sessionmaker(bind=banco())()
