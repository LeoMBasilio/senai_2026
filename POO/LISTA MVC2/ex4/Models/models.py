from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from datetime import datetime
import enum
import os

class Base(DeclarativeBase):
    pass

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "loja.db")


class StatusPedido(enum.Enum):
    ABERTO = "aberto"
    CONFIRMADO = "confirmado"
    CANCELADO = "cancelado"
    ENTREGUE = "entregue"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)

    pedidos = relationship("Pedido", back_populates="usuario")

    def __repr__(self):
        return f"Usuario(id={self.id}, nome={self.nome!r})"


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200), nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, default=0, nullable=False)

    itens = relationship("ItemPedido", back_populates="produto")

    def __repr__(self):
        return f"Produto(id={self.id}, nome={self.nome!r}, preco=R${self.preco:.2f}, estoque={self.estoque})"


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    status = Column(Enum(StatusPedido), default=StatusPedido.ABERTO, nullable=False)
    total = Column(Float, default=0.0, nullable=False)
    criado_em = Column(DateTime, default=datetime.now)

    usuario = relationship("Usuario", back_populates="pedidos")
    itens = relationship("ItemPedido", back_populates="pedido")

    def __repr__(self):
        return f"Pedido(id={self.id}, usuario={self.usuario_id}, total=R${self.total:.2f}, status={self.status.value})"


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)

    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="itens")

    @property
    def subtotal(self) -> float:
        return self.quantidade * self.preco_unitario

    def __repr__(self):
        return f"ItemPedido(produto={self.produto_id}, qtd={self.quantidade}, subtotal=R${self.subtotal:.2f})"


def banco():
    return create_engine(f"sqlite:///{DB_PATH}", echo=False)


def criar_tabelas():
    Base.metadata.create_all(banco())


def session():
    return sessionmaker(bind=banco())()
