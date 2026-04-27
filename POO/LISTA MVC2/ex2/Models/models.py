from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from datetime import datetime
import os

class Base(DeclarativeBase):
    pass

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "biblioteca.db")


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)

    emprestimos = relationship("Emprestimo", back_populates="usuario")

    def __repr__(self):
        return f"Usuario(id={self.id}, nome={self.nome!r})"


class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(150), nullable=False)
    disponivel = Column(Boolean, default=True, nullable=False)

    emprestimos = relationship("Emprestimo", back_populates="livro")

    def __repr__(self):
        status = "disponível" if self.disponivel else "emprestado"
        return f"Livro(id={self.id}, titulo={self.titulo!r}, status={status})"


class Emprestimo(Base):
    __tablename__ = "emprestimos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    livro_id = Column(Integer, ForeignKey("livros.id"), nullable=False)
    data_emprestimo = Column(DateTime, default=datetime.now, nullable=False)
    data_devolucao = Column(DateTime, nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)

    usuario = relationship("Usuario", back_populates="emprestimos")
    livro = relationship("Livro", back_populates="emprestimos")

    def __repr__(self):
        return (
            f"Emprestimo(id={self.id}, livro={self.livro_id}, "
            f"usuario={self.usuario_id}, ativo={self.ativo})"
        )


def banco():
    return create_engine(f"sqlite:///{DB_PATH}", echo=False)


def criar_tabelas():
    Base.metadata.create_all(banco())


def session():
    return sessionmaker(bind=banco())()
