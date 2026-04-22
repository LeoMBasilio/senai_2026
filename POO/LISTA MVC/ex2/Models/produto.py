# Models/produto.py — camada de dados do ex2
# Responsabilidade: definir a estrutura da tabela e as regras de negócio do Produto.

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# DeclarativeBase é a classe base do SQLAlchemy que mapeia classes Python → tabelas SQL.
# Toda model precisa herdar de Base para ser reconhecida pelo ORM.
class Base(DeclarativeBase):
    pass


class Produto(Base):
    __tablename__ = "produtos"  # nome da tabela no banco de dados

    id = Column(Integer, primary_key=True, autoincrement=True)  # chave primária gerada automaticamente
    nome = Column(String(100), nullable=False)                  # campo obrigatório (NOT NULL)

    # Os atributos _preco e _estoque usam underscore para indicar que são "privados".
    # O nome da coluna no banco é definido explicitamente ("preco", "estoque") porque
    # o SQLAlchemy usaria o nome do atributo Python (_preco) como nome da coluna por padrão.
    _preco = Column("preco", Float, nullable=False)
    _estoque = Column("estoque", Integer, nullable=False)

    def __init__(self, nome: str, preco: float, estoque: int):
        # A validação acontece no __init__ para garantir que nenhum objeto Produto
        # seja criado com valores inválidos, mesmo antes de chegar ao banco.
        if preco < 0:
            raise ValueError("Preço não pode ser negativo.")
        if estoque < 0:
            raise ValueError("Estoque não pode ser negativo.")
        self.nome = nome
        self._preco = preco
        self._estoque = estoque

    # @property transforma o método em um atributo de leitura.
    # Isso permite escrever produto.preco em vez de produto.get_preco().
    @property
    def preco(self) -> float:
        return self._preco

    # @preco.setter é chamado ao fazer produto.preco = valor.
    # Ele intercepta a atribuição e aplica a regra antes de salvar no atributo privado.
    @preco.setter
    def preco(self, valor: float):
        if valor < 0:
            raise ValueError("Preço não pode ser negativo.")
        self._preco = valor

    @property
    def estoque(self) -> int:
        return self._estoque

    @estoque.setter
    def estoque(self, valor: int):
        if valor < 0:
            raise ValueError("Estoque não pode ser negativo.")
        self._estoque = valor

    def __repr__(self):
        # __repr__ define como o objeto aparece ao ser impresso ou inspecionado no console.
        return f"Produto(id={self.id}, nome={self.nome!r}, preco={self._preco}, estoque={self._estoque})"

    @staticmethod
    def banco():
        # @staticmethod: não precisa de self nem de cls — é apenas uma função utilitária
        # agrupada dentro da classe por organização.
        # echo=False desliga os logs SQL no terminal (útil em produção).
        return create_engine("sqlite:///produtos.db", echo=False)

    @classmethod
    def criar_tabela(cls):
        # @classmethod recebe a própria classe (cls) como primeiro argumento.
        # create_all verifica se a tabela já existe antes de criá-la (idempotente).
        Base.metadata.create_all(cls.banco())

    @classmethod
    def session(cls):
        # sessionmaker cria uma fábrica de sessões vinculada ao engine.
        # Chamar ()() no final já retorna uma sessão aberta, pronta para uso.
        return sessionmaker(bind=cls.banco())()
