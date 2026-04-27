# Controllers/loja_controller.py — camada de lógica do ex4 (loja e-commerce)
# Responsabilidade: aplicar as regras de negócio da loja:
#   - Só adicionar itens a pedidos ABERTOS.
#   - Verificar e decrementar estoque ao adicionar itens.
#   - Restaurar estoque ao cancelar pedido.
#   - Não confirmar pedido vazio.

from sqlalchemy.orm import joinedload
from Models.base import Base, banco, session
from Models.usuario import Usuario
from Models.produto import Produto
from Models.pedido import Pedido
from Models.item_pedido import ItemPedido
from Models.status_pedido import StatusPedido


def inicializar():
    Base.metadata.create_all(banco())


def cadastrar_usuario(nome: str, email: str) -> Usuario:
    s = session()
    try:
        u = Usuario(nome=nome, email=email)
        s.add(u)
        s.commit()
        s.refresh(u)
        return u
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def cadastrar_produto(nome: str, preco: float, estoque: int) -> Produto:
    s = session()
    try:
        p = Produto(nome=nome, preco=preco, estoque=estoque)
        s.add(p)
        s.commit()
        s.refresh(p)
        return p
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def listar_produtos() -> list[Produto]:
    s = session()
    try:
        # Mostra apenas produtos com estoque positivo — sem estoque, não faz sentido exibir.
        return s.query(Produto).filter(Produto.estoque > 0).all()
    finally:
        s.close()


def abrir_pedido(usuario_id: int) -> Pedido:
    s = session()
    try:
        # Cria o pedido vazio — o cliente adiciona itens depois.
        pedido = Pedido(usuario_id=usuario_id)
        s.add(pedido)
        s.commit()
        s.refresh(pedido)
        return pedido
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def adicionar_item(pedido_id: int, produto_id: int, quantidade: int) -> ItemPedido:
    s = session()
    try:
        pedido = s.get(Pedido, pedido_id)
        if pedido is None:
            raise ValueError(f"Pedido {pedido_id} nao encontrado.")

        # Só pedidos ABERTOS aceitam novos itens — confirmado/cancelado são imutáveis.
        if pedido.status != StatusPedido.ABERTO:
            raise ValueError("So e possivel adicionar itens a pedidos em aberto.")

        produto = s.get(Produto, produto_id)
        if produto is None:
            raise ValueError(f"Produto {produto_id} nao encontrado.")

        # Valida o estoque antes de criar o item — evita venda de produto sem estoque.
        if produto.estoque < quantidade:
            raise ValueError(f"Estoque insuficiente. Disponivel: {produto.estoque}")

        item = ItemPedido(
            pedido_id=pedido_id,
            produto_id=produto_id,
            quantidade=quantidade,
            preco_unitario=produto.preco,  # congela o preço atual do produto no item
        )

        # Decrementa o estoque e acumula o total no pedido na mesma transação.
        produto.estoque -= quantidade
        pedido.total += item.subtotal
        s.add(item)
        s.commit()
        s.refresh(item)
        return item
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def confirmar_pedido(pedido_id: int) -> Pedido:
    s = session()
    try:
        pedido = s.get(Pedido, pedido_id)
        if pedido is None:
            raise ValueError(f"Pedido {pedido_id} nao encontrado.")
        if pedido.status != StatusPedido.ABERTO:
            raise ValueError("Apenas pedidos em aberto podem ser confirmados.")

        # Não confirma pedido vazio — sem itens não há compra.
        if not pedido.itens:
            raise ValueError("Nao e possivel confirmar um pedido vazio.")

        pedido.status = StatusPedido.CONFIRMADO
        s.commit()
        s.refresh(pedido)
        return pedido
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def cancelar_pedido(pedido_id: int) -> Pedido:
    s = session()
    try:
        pedido = s.get(Pedido, pedido_id)
        if pedido is None:
            raise ValueError(f"Pedido {pedido_id} nao encontrado.")

        # Pedido ENTREGUE não pode ser cancelado — só ABERTO ou CONFIRMADO.
        if pedido.status not in (StatusPedido.ABERTO, StatusPedido.CONFIRMADO):
            raise ValueError("Pedido nao pode ser cancelado.")

        # Devolve o estoque de cada item ao produto original.
        for item in pedido.itens:
            produto = s.get(Produto, item.produto_id)
            produto.estoque += item.quantidade

        pedido.status = StatusPedido.CANCELADO
        s.commit()
        s.refresh(pedido)
        return pedido
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def listar_pedidos_usuario(usuario_id: int) -> list[Pedido]:
    s = session()
    try:
        # joinedload carrega os itens de cada pedido em uma única query (JOIN)
        # em vez de fazer um SELECT extra para cada pedido (N+1 queries).
        return (
            s.query(Pedido)
            .options(joinedload(Pedido.itens))
            .filter(Pedido.usuario_id == usuario_id)
            .all()
        )
    finally:
        s.close()
