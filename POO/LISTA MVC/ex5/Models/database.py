from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Models.base import Base
import Models.produto     # noqa: F401 — registra Produto no metadata do Base
import Models.pedido      # noqa: F401 — registra Pedido no metadata do Base
import Models.item_pedido  # noqa: F401 — registra ItemPedido no metadata do Base

ENGINE = create_engine("sqlite:///pedidos.db", echo=False)


def criar_tabelas():
    Base.metadata.create_all(ENGINE)


def get_session():
    return sessionmaker(bind=ENGINE)()
