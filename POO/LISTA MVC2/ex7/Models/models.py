from sqlalchemy import Column, Integer, String, Float, Text, Enum, Boolean, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from datetime import datetime
import enum
import os

class Base(DeclarativeBase):
    pass

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "viloes.db")


class StatusCrime(enum.Enum):
    PLANEJADO = "planejado"
    EM_EXECUCAO = "em_execucao"
    CONCLUIDO = "concluido"
    FALHOU = "falhou"


class Vilao(Base):
    __tablename__ = "viloes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    codinome = Column(String(100), nullable=True)
    poder_mundial = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)

    capangas = relationship("Capanga", back_populates="vilao")
    crimes = relationship("Crime", back_populates="vilao")
    dominio = relationship("DominioCriminal", back_populates="vilao", uselist=False)

    def __repr__(self):
        return f"Vilao(id={self.id}, nome={self.nome!r}, poder={self.poder_mundial})"


class Capanga(Base):
    __tablename__ = "capangas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    habilidade = Column(String(100), nullable=False)
    lealdade = Column(Integer, default=100)
    vilao_id = Column(Integer, ForeignKey("viloes.id"), nullable=False)

    vilao = relationship("Vilao", back_populates="capangas")

    def __repr__(self):
        return f"Capanga(id={self.id}, nome={self.nome!r}, habilidade={self.habilidade!r})"


class Crime(Base):
    __tablename__ = "crimes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=True)
    recompensa_poder = Column(Integer, default=10)
    status = Column(Enum(StatusCrime), default=StatusCrime.PLANEJADO, nullable=False)
    planejado_em = Column(DateTime, default=datetime.now)
    executado_em = Column(DateTime, nullable=True)
    vilao_id = Column(Integer, ForeignKey("viloes.id"), nullable=False)

    vilao = relationship("Vilao", back_populates="crimes")

    def __repr__(self):
        return f"Crime(id={self.id}, nome={self.nome!r}, status={self.status.value})"


class DominioCriminal(Base):
    __tablename__ = "dominios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vilao_id = Column(Integer, ForeignKey("viloes.id"), unique=True, nullable=False)
    territorio = Column(String(200), default="Esconderijo Secreto")
    pontos_dominio = Column(Float, default=0.0)

    vilao = relationship("Vilao", back_populates="dominio")

    def __repr__(self):
        return f"Dominio(vilao={self.vilao_id}, territorio={self.territorio!r}, pontos={self.pontos_dominio})"


def banco():
    return create_engine(f"sqlite:///{DB_PATH}", echo=False)


def criar_tabelas():
    Base.metadata.create_all(banco())


def session():
    return sessionmaker(bind=banco())()
