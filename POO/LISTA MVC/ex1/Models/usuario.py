from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)

    def __repr__(self):
        return f"Usuario(id={self.id}, nome={self.nome!r}, email={self.email!r})"

    @staticmethod
    def banco():
        return create_engine("sqlite:///usuarios.db", echo=False)

    @classmethod
    def criar_tabela(cls):
        Base.metadata.create_all(cls.banco())

    @classmethod
    def session(cls):
        return sessionmaker(bind=cls.banco())()
