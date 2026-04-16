'''
    Exercício 1 – Primeiro Modelo (Usuário)
    Crie um modelo Usuario com id, nome e email (único). Implemente criação da tabela, inserção de 3
    usuários e listagem.
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column

class Conexao:
    def __init__(self, url):
        self.__engine = create_engine(url)

    def get_engine(self):
        return self.__engine

class Base(DeclarativeBase):
    pass

class Usuario(Base):
    __tablename__ = 'usuarios'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)

if __name__ == "__main__":
    conexao = Conexao('sqlite:///usuarios.db')
    Base.metadata.create_all(conexao.get_engine())

    with Session(conexao.get_engine()) as session:

        print("1. Adicionar usuário")
        print("2. Listar usuários")
        op = input("Escolha uma opção: ")

        match op:
            case '1':
                nome = input("Nome: ")
                email = input("Email: ")
                usuario = Usuario(nome=nome, email=email)
                session.add(usuario)
                session.commit()
                print("Usuário adicionado!")
            case '2':
                usuarios = session.query(Usuario).all()
                for u in usuarios:
                    print(f"{u.id}: {u.nome} - {u.email}")
