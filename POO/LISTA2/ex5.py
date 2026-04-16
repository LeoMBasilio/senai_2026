'''
Exercício 5 – Relacionamento com Mais Dados
Modelos Pedido, ItemPedido e Produto. Calcular total do pedido.
'''

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column, relationship


class Banco:
    def __init__(self, url: str):
        self.engine = create_engine(url)

    def get_engine(self):
        return self.engine


class Base(DeclarativeBase):
    pass


class Produto(Base):
    __tablename__ = 'produtos'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    preco: Mapped[float] = mapped_column()
    itens: Mapped[list['ItemPedido']] = relationship(back_populates='produto')


class Pedido(Base):
    __tablename__ = 'pedidos'
    id: Mapped[int] = mapped_column(primary_key=True)
    descricao: Mapped[str] = mapped_column()
    itens: Mapped[list['ItemPedido']] = relationship(back_populates='pedido')

    def calcular_total(self) -> float:
        return sum(item.quantidade * item.produto.preco for item in self.itens)
    
        # O MESMO CÓDIGO DE CIMA, MAS COM MAIS LINHAS PARA FICAR MAIS LEGÍVEL
        # for item in self.itens:
        #     subtotal = item.quantidade * item.produto.preco
        #     total += subtotal
        #     return total

class ItemPedido(Base):
    __tablename__ = 'itens_pedido'
    id: Mapped[int] = mapped_column(primary_key=True)
    quantidade: Mapped[int] = mapped_column()
    produto_id: Mapped[int] = mapped_column(ForeignKey('produtos.id'))
    pedido_id: Mapped[int] = mapped_column(ForeignKey('pedidos.id'))
    produto: Mapped['Produto'] = relationship(back_populates='itens')
    pedido: Mapped['Pedido'] = relationship(back_populates='itens')


def menu():
    print('\n=== SISTEMA DE PEDIDOS ===')
    print('1. Cadastrar produto')
    print('2. Criar pedido')
    print('3. Adicionar item ao pedido')
    print('4. Ver total do pedido')
    print('0. Sair')
    return int(input('Escolha uma opção: '))


def Adicninar_iten_pedido(pedido_id):
    pedido = session.query(Pedido).filter_by(id=pedido_id).first()
    if not pedido:
        print('Pedido não encontrado.')
        return False

    produtos = session.query(Produto).all()
    if not produtos:
        print('Nenhum produto cadastrado.')
        return False

    print('\nProdutos disponíveis:')
    for p in produtos:
        print(f'  [{p.id}] {p.nome} - R$ {p.preco:.2f}')

    produto_id = int(input('ID do produto: '))
    produto = session.query(Produto).filter_by(id=produto_id).first()
    if not produto:
        print('Produto não encontrado.')
        return False

    quantidade = int(input('Quantidade: '))
    item = ItemPedido(quantidade=quantidade, produto=produto, pedido=pedido)
    session.add(item)
    session.commit()
    return f'{quantidade}x "{produto.nome}" adicionado ao pedido #{pedido_id}.'

if __name__ == "__main__":
    banco = Banco('sqlite:///ex5.db')
    Base.metadata.create_all(banco.get_engine())

    while True:
        op = menu()

        with Session(banco.get_engine()) as session:
            match op:
                case 0:
                    print('Encerrando...')
                    break

                case 1:
                    nome = input('Nome do produto: ')
                    preco = float(input('Preço do produto: R$ '))
                    produto = Produto(nome=nome, preco=preco)
                    session.add(produto)
                    session.commit()
                    print(f'Produto "{nome}" cadastrado com sucesso!')

                case 2:
                    descricao = input('Descrição do pedido: ')
                    pedido = Pedido(descricao=descricao)
                    session.add(pedido)
                    session.commit()
                    print(f'Pedido #{pedido.id} criado com sucesso!')

                    op = int(input('Deseja adicionar itens a este pedido? (1-Sim / 0-Não): '))
                    if op == 1:
                        Adicninar_iten_pedido(pedido.id)
                    else:
                        continue

                case 3:
                    pedido_id = int(input('ID do pedido: '))
                    if not Adicninar_iten_pedido(pedido_id):
                        continue                    

                case 4:
                    pedido_id = int(input('ID do pedido: '))
                    pedido = session.query(Pedido).filter_by(id=pedido_id).first()
                    if not pedido:
                        print('Pedido não encontrado.')
                        continue

                    print(f'\nPedido #{pedido.id} – {pedido.descricao}')
                    print('-' * 35)
                    if not pedido.itens:
                        print('Nenhum item neste pedido.')
                    else:
                        for item in pedido.itens:
                            subtotal = item.quantidade * item.produto.preco
                            print(f'  {item.produto.nome:20} {item.quantidade}x R$ {item.produto.preco:.2f} = R$ {subtotal:.2f}')
                        print('-' * 35)
                        print(f'  {"TOTAL":20} R$ {pedido.calcular_total():.2f}')

                case _:
                    print('Opção inválida.')