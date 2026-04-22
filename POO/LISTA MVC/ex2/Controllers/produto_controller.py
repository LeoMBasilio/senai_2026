# Controllers/produto_controller.py — camada de lógica do ex2
# Responsabilidade: orquestrar operações no banco sem expor detalhes de SQL à View.
# O Controller nunca imprime nada — só processa e devolve dados.

from Models.produto import Produto


def inicializar():
    # Cria a tabela caso ela ainda não exista. Deve ser chamada uma vez no início do programa.
    Produto.criar_tabela()


def inserir_produto(nome: str, preco: float, estoque: int) -> Produto:
    s = Produto.session()
    try:
        # O construtor de Produto já valida os valores (encapsulamento).
        # Se preco ou estoque forem negativos, ValueError é lançado aqui.
        produto = Produto(nome=nome, preco=preco, estoque=estoque)
        s.add(produto)      # agenda o INSERT
        s.commit()          # executa o INSERT no banco
        s.refresh(produto)  # recarrega o objeto com o id gerado pelo banco
        return produto
    except Exception as e:
        s.rollback()  # desfaz qualquer alteração pendente em caso de erro
        raise e
    finally:
        s.close()  # sempre fecha a sessão para liberar a conexão


def atualizar_preco(produto_id: int, novo_preco: float) -> Produto:
    s = Produto.session()
    try:
        produto = s.query(Produto).filter_by(id=produto_id).first()
        if not produto:
            raise ValueError(f"Produto {produto_id} não encontrado.")
        # Usa o setter com validação — não atribuímos direto em _preco.
        produto.preco = novo_preco
        s.commit()
        s.refresh(produto)
        return produto
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def atualizar_estoque(produto_id: int, novo_estoque: int) -> Produto:
    s = Produto.session()
    try:
        produto = s.query(Produto).filter_by(id=produto_id).first()
        if not produto:
            raise ValueError(f"Produto {produto_id} não encontrado.")
        produto.estoque = novo_estoque  # passa pelo setter que valida negativos
        s.commit()
        s.refresh(produto)
        return produto
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def listar_produtos() -> list[Produto]:
    s = Produto.session()
    try:
        # .all() executa SELECT * FROM produtos e retorna uma lista de objetos Produto.
        return s.query(Produto).all()
    finally:
        s.close()
