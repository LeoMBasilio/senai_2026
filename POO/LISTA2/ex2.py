'''
Exercício 2 – Encapsulamento com Regra
Modelo Produto com id, nome, preco, estoque. Não permitir valores negativos. Métodos para
atualizar.
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column

class Banco:
    def __init__(self, url):
      self.__engine = create_engine(url)

    def get_engine(self):
        return self.__engine
    
class Base(DeclarativeBase):
    pass

class Produto(Base):
    __tablename__ = 'produtos'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    preco: Mapped[float] = mapped_column()
    estoque: Mapped[int] = mapped_column()

    def __init__(self, nome, preco, estoque):
        self.nome = nome
        self.set_preco(preco)
        self.set_estoque(estoque)

    def set_preco(self, preco):
        if preco < 0:
            raise ValueError("Preço não pode ser negativo.")
        self.preco = preco

    def set_estoque(self, estoque):
        if estoque < 0:
            raise ValueError("Estoque não pode ser negativo.")
        self.estoque = estoque

if __name__ == "__main__":
    banco = Banco('sqlite:///produtos.db')
    Base.metadata.create_all(banco.get_engine())

    with Session(banco.get_engine()) as session:
        print('1. adicionar produto')
        print('2. atualizar produto')
        print('3. listar produtos')
        op = int(input('Escolha uma opção: '))

        match op:
            case 1:
                nome = input('Nome do produto: ')
                preco = float(input('Preço do produto: '))
                estoque = int(input('Estoque do produto: '))
                produto = Produto(nome, preco, estoque)
                session.add(produto)
                session.commit()
            case 2:
                id = int(input('ID do produto a atualizar: '))
                produto = session.query(Produto).filter_by(id=id).first()
                if produto:
                    preco = float(input('Novo preço do produto: '))
                    estoque = int(input('Novo estoque do produto: '))
                    produto.set_preco(preco)
                    produto.set_estoque(estoque)
                    session.commit()
                else:
                    print('Produto não encontrado.')
            case 3:
                produtos = session.query(Produto).all()
                for p in produtos:
                    print(f'ID: {p.id}, Nome: {p.nome}, Preço: {p.preco}, Estoque: {p.estoque}')
