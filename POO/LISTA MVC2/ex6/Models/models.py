from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from datetime import datetime
import os

class Base(DeclarativeBase):
    pass

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tempo.db")


class Viajante(Base):
    __tablename__ = "viajantes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    ano_base = Column(Integer, nullable=False, default=2025)

    viagens = relationship("Viagem", back_populates="viajante")

    def __repr__(self):
        return f"Viajante(id={self.id}, nome={self.nome!r}, ano_base={self.ano_base})"


class LinhaTempo(Base):
    __tablename__ = "linhas_tempo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    descricao = Column(Text, nullable=True)
    original = Column(Boolean, default=False)
    criada_em = Column(DateTime, default=datetime.now)
    origem_viagem_id = Column(Integer, ForeignKey("viagens.id"), nullable=True)

    eventos = relationship("Evento", back_populates="linha_tempo")
    origem_viagem = relationship("Viagem", back_populates="linhas_geradas", foreign_keys=[origem_viagem_id])

    def __repr__(self):
        tag = " [ORIGINAL]" if self.original else ""
        return f"LinhaTempo(id={self.id}, nome={self.nome!r}{tag})"


class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(300), nullable=False)
    ano = Column(Integer, nullable=False)
    alterado = Column(Boolean, default=False)
    descricao_original = Column(String(300), nullable=True)
    linha_tempo_id = Column(Integer, ForeignKey("linhas_tempo.id"), nullable=False)

    linha_tempo = relationship("LinhaTempo", back_populates="eventos")

    def __repr__(self):
        tag = " [ALTERADO]" if self.alterado else ""
        return f"Evento(ano={self.ano}, desc={self.descricao!r}{tag})"


class Viagem(Base):
    __tablename__ = "viagens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    viajante_id = Column(Integer, ForeignKey("viajantes.id"), nullable=False)
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    ano_destino = Column(Integer, nullable=False)
    alteracao = Column(Text, nullable=False)
    realizada_em = Column(DateTime, default=datetime.now)

    viajante = relationship("Viajante", back_populates="viagens")
    linhas_geradas = relationship("LinhaTempo", back_populates="origem_viagem", foreign_keys=[LinhaTempo.origem_viagem_id])

    def __repr__(self):
        return f"Viagem(viajante={self.viajante_id}, ano={self.ano_destino}, alteracao={self.alteracao!r})"


def banco():
    return create_engine(f"sqlite:///{DB_PATH}", echo=False)


def criar_tabelas():
    Base.metadata.create_all(banco())


def session():
    return sessionmaker(bind=banco())()
