# Models/usuario.py — camada de dados do ex1
# Responsabilidade: definir como o objeto Usuario é armazenado no banco.
# A Model não contém lógica de negócio — só estrutura e conexão com o banco.

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# DeclarativeBase é a "fábrica de modelos" do SQLAlchemy.
# Toda classe que herdar de Base será mapeada para uma tabela no banco.
class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = "usuarios"  # nome da tabela que será criada no SQLite

    # Column(Integer, primary_key=True, autoincrement=True): o banco gera o id
    # automaticamente a cada INSERT — não precisamos passar o id manualmente.
    id = Column(Integer, primary_key=True, autoincrement=True)

    # nullable=False equivale ao NOT NULL do SQL — o campo é obrigatório.
    nome = Column(String(100), nullable=False)

    # unique=True garante que dois usuários não podem ter o mesmo email no banco.
    email = Column(String(150), nullable=False, unique=True)

    def __repr__(self):
        # __repr__ define como o objeto aparece quando impresso/inspecionado no console.
        # !r coloca aspas ao redor das strings para distinguir de None ou números.
        return f"Usuario(id={self.id}, nome={self.nome!r}, email={self.email!r})"

    @staticmethod
    def banco():
        # @staticmethod: não usa self nem cls — é apenas uma função agrupada na classe.
        # create_engine cria a conexão com o banco SQLite (arquivo usuarios.db na pasta atual).
        # echo=False desliga os logs SQL no terminal.
        return create_engine("sqlite:///usuarios.db", echo=False)

    @classmethod
    def criar_tabela(cls):
        # @classmethod recebe a classe (cls) como primeiro argumento, não uma instância.
        # create_all cria todas as tabelas registradas no Base — é idempotente:
        # se a tabela já existir, ele não recria nem apaga os dados.
        Base.metadata.create_all(cls.banco())

    @classmethod
    def session(cls):
        # sessionmaker cria uma "fábrica" de sessões vinculada ao engine.
        # Chamar ()() no final já retorna uma sessão aberta e pronta para uso.
        # Cada sessão representa uma transação — operações dentro dela são confirmadas
        # com commit() ou desfeitas com rollback().
        return sessionmaker(bind=cls.banco())()
