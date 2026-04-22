# Controllers/produto_controller.py — camada de lógica do ex3
# Foco: busca por nome com LIKE e filtro por preço mínimo.

from Models.produto import Produto


def inicializar():
    Produto.criar_tabela()


def inserir_produto(nome: str, preco: float, estoque: int) -> Produto:
    s = Produto.session()
    try:
        produto = Produto(nome=nome, preco=preco, estoque=estoque)
        s.add(produto)
        s.commit()
        s.refresh(produto)
        return produto
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def buscar_por_nome(termo: str) -> list[Produto]:
    s = Produto.session()
    try:
        # .ilike() faz busca case-insensitive (maiúsculas e minúsculas tratadas igual).
        # Os % em volta do termo são curingas SQL: %notebook% encontra qualquer string
        # que contenha "notebook" em qualquer posição — equivale ao LIKE '%notebook%' no SQL.
        return s.query(Produto).filter(Produto.nome.ilike(f"%{termo}%")).all()
    finally:
        s.close()


def listar_por_preco_maior_que(valor: float) -> list[Produto]:
    s = Produto.session()
    try:
        # .filter() com operador > gera WHERE preco > :valor no SQL.
        # O SQLAlchemy converte o operador Python > em SQL automaticamente.
        return s.query(Produto).filter(Produto.preco > valor).all()
    finally:
        s.close()
