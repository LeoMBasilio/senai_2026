from sqlalchemy import Column, Integer, String, Float

from Models.base import Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)

    def __repr__(self):
        return f"Produto(id={self.id}, nome={self.nome!r}, preco={self.preco})"
