from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime, CheckConstraint, create_engine
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from datetime import datetime
import os

class Base(DeclarativeBase):
    pass

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "filmes.db")


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)

    avaliacoes = relationship("Avaliacao", back_populates="usuario")

    def __repr__(self):
        return f"Usuario(id={self.id}, nome={self.nome!r})"


class Filme(Base):
    __tablename__ = "filmes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    ano = Column(Integer, nullable=False)
    genero = Column(String(100), nullable=True)
    diretor = Column(String(150), nullable=True)

    avaliacoes = relationship("Avaliacao", back_populates="filme")

    def __repr__(self):
        return f"Filme(id={self.id}, titulo={self.titulo!r}, ano={self.ano})"


class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filme_id = Column(Integer, ForeignKey("filmes.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nota = Column(Float, nullable=False)
    comentario = Column(Text, nullable=True)
    criada_em = Column(DateTime, default=datetime.now)

    __table_args__ = (
        CheckConstraint("nota >= 0 AND nota <= 10", name="nota_valida"),
    )

    filme = relationship("Filme", back_populates="avaliacoes")
    usuario = relationship("Usuario", back_populates="avaliacoes")

    def __repr__(self):
        return f"Avaliacao(filme={self.filme_id}, usuario={self.usuario_id}, nota={self.nota})"


def banco():
    return create_engine(f"sqlite:///{DB_PATH}", echo=False)


def criar_tabelas():
    Base.metadata.create_all(banco())


def session():
    return sessionmaker(bind=banco())()
