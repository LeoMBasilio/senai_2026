from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from datetime import datetime
import enum
import os

class Base(DeclarativeBase):
    pass

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tarefas.db")


class StatusTarefa(enum.Enum):
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    tarefas = relationship("Tarefa", back_populates="usuario")

    def __repr__(self):
        return f"Usuario(id={self.id}, nome={self.nome!r})"


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)
    descricao = Column(String(255), nullable=True)

    tarefas = relationship("Tarefa", back_populates="categoria")

    def __repr__(self):
        return f"Categoria(id={self.id}, nome={self.nome!r})"


class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    descricao = Column(String(500), nullable=True)
    status = Column(Enum(StatusTarefa), default=StatusTarefa.PENDENTE, nullable=False)
    criada_em = Column(DateTime, default=datetime.now)
    atualizada_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="tarefas")
    categoria = relationship("Categoria", back_populates="tarefas")

    def __repr__(self):
        return f"Tarefa(id={self.id}, titulo={self.titulo!r}, status={self.status.value})"


def banco():
    return create_engine(f"sqlite:///{DB_PATH}", echo=False)


def criar_tabelas():
    Base.metadata.create_all(banco())


def session():
    return sessionmaker(bind=banco())()
