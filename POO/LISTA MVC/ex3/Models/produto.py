# Models/produto.py — camada de dados do ex3
# Versão simplificada sem encapsulamento: aqui o foco é busca e filtro, não regras de campo.

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)    # coluna pública — sem setter aqui
    estoque = Column(Integer, nullable=False)

    def __repr__(self):
        return f"Produto(id={self.id}, nome={self.nome!r}, preco={self.preco}, estoque={self.estoque})"

    @staticmethod
    def banco():
        return create_engine("sqlite:///produtos.db", echo=False)

    @classmethod
    def criar_tabela(cls):
        Base.metadata.create_all(cls.banco())

    @classmethod
    def session(cls):
        return sessionmaker(bind=cls.banco())()
