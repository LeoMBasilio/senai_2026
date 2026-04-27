from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from Models.base import Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200), nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, default=0, nullable=False)

    itens = relationship("ItemPedido", back_populates="produto")

    def __repr__(self):
        return f"Produto(id={self.id}, nome={self.nome!r}, preco=R${self.preco:.2f}, estoque={self.estoque})"
