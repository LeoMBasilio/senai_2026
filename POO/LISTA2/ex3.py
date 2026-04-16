'''
Exercício 3 – Busca e Filtro
Buscar produto por nome (LIKE) e listar produtos com preço maior que X.
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column

class Banco:
    def __init__(self, url):
        self.engine = create_engine(url)

class Base(DeclarativeBase):
    pass

class Produto(Base):
    __tablename__ = 'produtos'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    preco: Mapped[float] = mapped_column()

    def __repr__(self) -> str:
        return f"Produto(id={self.id}, nome='{self.nome}', preco={self.preco})"
    
if __name__ == "__main__":
    banco = Banco('sqlite:///produtos.db')
    Base.metadata.create_all(banco.engine)

    with Session(banco.engine) as session:
        print('1. adicionar produto')
        print('2. atualizar produto')
        print('3. listar produtos')
        print('4. buscar produto por nome')
        print('5. filtrar produtos por preço')
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

            case 4:
                nome = input('Nome do produto para busca: ')
                produtos = session.query(Produto).filter(Produto.nome.like(f'%{nome}%')).all()
                for p in produtos:
                    print(f'ID: {p.id}, Nome: {p.nome}, Preço: {p.preco}, Estoque: {p.estoque}')
            case 5:
                preco = float(input('Preço mínimo: '))
                produtos = session.query(Produto).filter(Produto.preco > preco).all()
                for p in produtos:
                    print(f'ID: {p.id}, Nome: {p.nome}, Preço: {p.preco}, Estoque: {p.estoque}')