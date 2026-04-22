# Controllers/pedido_controller.py — camada de lógica do ex5
# Gerencia a criação de pedidos com múltiplos itens e o cálculo do total.

from Models.produto import Produto
from Models.pedido import Pedido
from Models.item_pedido import ItemPedido
from Models.database import criar_tabelas, get_session


def inicializar():
    criar_tabelas()


def inserir_produto(nome: str, preco: float) -> Produto:
    s = get_session()
    try:
        produto = Produto(nome=nome, preco=preco)
        s.add(produto)
        s.commit()
        s.refresh(produto)
        return produto
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def criar_pedido(itens: list[tuple[int, int]]) -> tuple[Pedido, list[ItemPedido], float]:
    """itens: lista de (produto_id, quantidade)"""
    s = get_session()
    try:
        # Cria o Pedido vazio primeiro para obter o id gerado pelo banco.
        pedido = Pedido()
        s.add(pedido)
        # flush() envia o INSERT ao banco sem fazer commit — o pedido recebe um id
        # mas a transação ainda está aberta. Isso permite usar pedido.id nos itens.
        s.flush()

        itens_criados = []
        for produto_id, quantidade in itens:
            produto = s.query(Produto).filter_by(id=produto_id).first()
            if not produto:
                raise ValueError(f"Produto {produto_id} não encontrado.")
            item = ItemPedido(
                pedido_id=pedido.id,
                produto_id=produto_id,
                quantidade=quantidade,
                preco_unitario=produto.preco,  # congela o preço atual do produto
            )
            s.add(item)
            itens_criados.append(item)

        s.commit()
        s.refresh(pedido)

        # O total é calculado em Python — evita uma query extra ao banco.
        total = sum(i.quantidade * i.preco_unitario for i in itens_criados)
        return pedido, itens_criados, total
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def calcular_total_pedido(pedido_id: int) -> float:
    s = get_session()
    try:
        # Busca os itens pelo pedido_id e soma quantidade × preço unitário.
        itens = s.query(ItemPedido).filter_by(pedido_id=pedido_id).all()
        return sum(i.quantidade * i.preco_unitario for i in itens)
    finally:
        s.close()
