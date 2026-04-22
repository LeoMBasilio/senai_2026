# Models/pagamento.py — camada de dados do ex7
# Demonstra herança de tabelas no SQLAlchemy com a estratégia "joined table inheritance".
# A tabela pai (pagamentos) guarda os campos comuns; cada subclasse tem sua própria tabela
# com os campos específicos, ligada à pai pelo mesmo id.

from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Float, nullable=False)

    # A coluna "tipo" é o discriminador — o SQLAlchemy a usa para saber qual
    # subclasse instanciar ao carregar um registro do banco.
    tipo = Column(String(20), nullable=False)

    __mapper_args__ = {
        "polymorphic_on": tipo,           # coluna que diferencia as subclasses
        "polymorphic_identity": "pagamento",  # valor gravado na coluna "tipo" para esta classe
    }

    def processar_pagamento(self) -> str:
        # Método definido na base para garantir a interface — subclasses DEVEM sobrescrever.
        raise NotImplementedError("Subclasse deve implementar processar_pagamento.")

    def __repr__(self):
        return f"Pagamento(id={self.id}, valor={self.valor}, tipo={self.tipo})"


class Cartao(Pagamento):
    __tablename__ = "pagamentos_cartao"

    # O id aqui é FK para pagamentos.id — é o que liga as duas tabelas no JOIN.
    id = Column(Integer, primary_key=True)
    numero_cartao = Column(String(20), nullable=False)
    bandeira = Column(String(20), nullable=False)

    __mapper_args__ = {"polymorphic_identity": "cartao"}  # valor gravado em pagamentos.tipo

    def processar_pagamento(self) -> str:
        # Sobrescreve o método base com a lógica específica de cartão.
        # [-4:] exibe apenas os últimos 4 dígitos por segurança.
        return f"Pagamento de R${self.valor:.2f} processado via cartão {self.bandeira} (**** {self.numero_cartao[-4:]})"


class Pix(Pagamento):
    __tablename__ = "pagamentos_pix"

    id = Column(Integer, primary_key=True)
    chave_pix = Column(String(100), nullable=False)

    __mapper_args__ = {"polymorphic_identity": "pix"}

    def processar_pagamento(self) -> str:
        return f"Pagamento de R${self.valor:.2f} processado via Pix (chave: {self.chave_pix})"


ENGINE = create_engine("sqlite:///pagamentos.db", echo=False)


def criar_tabelas():
    Base.metadata.create_all(ENGINE)


def get_session():
    return sessionmaker(bind=ENGINE)()
