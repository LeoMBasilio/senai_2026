from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Banco:
    def __init__(self, url):
        self.__engine = create_engine(url)
    def get_engine(self):
        return self.__engine
    
class Base(DeclarativeBase):
    pass

class Contatos(Base):

    __tablename__ = 'contatos'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    email: Mapped[str]
    telefone: Mapped[int]

if __name__ == '__main__':
    bd = Banco('sqlite:///contatos.db')
    Base.metadata.create_all(bd.get_engine())

    with Session(bd.get_engine()) as session:
        while True:
            print('1 - Adicionar contato')
            print('2 - Listar contatos')
            print('3 - Atualizar contato')
            print('4 - Deletar contato')
            print('5 - Buscar contato por id')
            print('0 - Sair')

            op = int(input('Escolha uma opção: '))


            match op:
                case 1:
                    nome = input('Digite o nome do contato: ')
                    email = input('Digite o email do contato: ')
                    telefone = int(input('Digite o telefone do contato: '))

                    contato = Contatos(nome=nome, email=email, telefone=telefone)
                    session.add(contato)
                    session.commit()
                    print('Contato adicionado com sucesso!')
                case 2:
                    contato = session.query(Contatos).all()

                    print('Contatos:')
                    print('ID | Nome | Email | Telefone')
                    for c in contato:
                        print(f'{c.id} | {c.nome} | {c.email} | {c.telefone}')
                case 3:
                    id = int(input("Id: "))
                    contato = session.query(Contatos).filter_by(id=id).first()

                    if contato:
                        nome = input('Digite o nome do contato: ')
                        email = input('Digite o email do contato: ')
                        telefone = int(input('Digite o telefone do contato: '))

                        contato.nome = nome 
                        contato.email = email 
                        contato.telefone = telefone

                        session.commit()
                        print('Contato atualizado com sucesso!')
                    else:
                        print('Contato não encontrado!')

                case 4:
                    id = int(input("Id: "))
                    contato = session.query(Contatos).filter_by(id=id).first()

                    if contato:
                        session.delete(contato)
                        session.commit()
                        print('Contato deletado com sucesso!')
                    else:
                        print('Contato não encontrado!')

                case 5:
                    id = int(input("Id: "))
                    contato = session.query(Contatos).filter_by(id=id).first()

                    if contato:
                        print(f'ID: {contato.id}')
                        print(f'Nome: {contato.nome}')
                        print(f'Email: {contato.email}')
                        print(f'Telefone: {contato.telefone}')
                    else:
                        print('Contato não encontrado!')

                case 0:
                    print('Saindo...')
                    break