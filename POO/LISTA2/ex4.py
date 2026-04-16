'''
Exercício 4 – Relacionamento 1:N
Modelos Cliente e Pedido. Um cliente tem vários pedidos. Listar pedidos por cliente.
'''

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column, relationship

class Banco:
    def __init__(self, url):
        self.engine = create_engine(url)

    def get_engine(self):
        return self.engine
    
class Base(DeclarativeBase):
    pass

class Pedido(Base):
    __tablename__ = 'pedidos'
    id: Mapped[int] = mapped_column(primary_key=True)
    descricao: Mapped[str] = mapped_column()
    cliente_id: Mapped[int] = mapped_column(ForeignKey('clientes.id'))
    cliente: Mapped['Cliente'] = relationship(back_populates='pedidos')

class Cliente(Base):
    __tablename__ = 'clientes'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    pedidos: Mapped[list['Pedido']] = relationship(back_populates='cliente')


if __name__ == "__main__":
    banco = Banco('sqlite:///ex4.db')
    Base.metadata.create_all(banco.get_engine())

    with Session(banco.get_engine()) as session:
        print('1. Adcionar clientes')
        print('2. Adicionar pedidos')
        print('3. Listar pedidos por cliente')

        op = int(input('Escolha uma opção: '))

        match op:
            case 1:
                nome = input('Digite o nome do cliente: ')
                cliente = Cliente(nome=nome)
                session.add(cliente)
                session.commit()

            case 2:
                cliente_id = input('Digite o ID do cliente: ')
                cliente = session.query(Cliente).filter_by(id=cliente_id).first()
                if cliente:
                    descricao = input('Digite a descrição do pedido: ')
                    pedido = Pedido(descricao=descricao, cliente=cliente)
                    session.add(pedido)
                    session.commit()
                else:
                    print('Cliente não encontrado.')
            case 3:
                clientes = session.query(Cliente).all()
                for cliente in clientes:
                    print(f'Cliente: {cliente.nome}')
                    for pedido in cliente.pedidos:
                        print(f'  Pedido: {pedido.descricao}')
            