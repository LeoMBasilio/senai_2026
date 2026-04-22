# Models/usuario.py — camada de dados do ex9
# Armazena apenas o hash da senha — jamais a senha em texto puro.
# Isso garante que, mesmo com acesso direto ao banco, as senhas permanecem protegidas.

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(150), nullable=False, unique=True)  # email é o identificador de login

    # senha_hash tem tamanho 256 para comportar o hex de SHA-256 (64 caracteres).
    # O campo se chama senha_hash (não senha) para deixar explícito que não é texto puro.
    senha_hash = Column(String(256), nullable=False)

    def __repr__(self):
        return f"Usuario(id={self.id}, email={self.email!r})"

    @staticmethod
    def banco():
        return create_engine("sqlite:///auth.db", echo=False)

    @classmethod
    def criar_tabela(cls):
        Base.metadata.create_all(cls.banco())

    @classmethod
    def session(cls):
        return sessionmaker(bind=cls.banco())()
