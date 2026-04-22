# Controllers/loja_controller.py — camada de lógica do ex4
# Gerencia operações de Cliente e Pedido, expondo a relação 1:N ao main.

from Models.cliente import Cliente
from Models.pedido import Pedido
from Models.database import criar_tabelas, get_session


def inicializar():
    criar_tabelas()


def inserir_cliente(nome: str, email: str) -> Cliente:
    s = get_session()
    try:
        cliente = Cliente(nome=nome, email=email)
        s.add(cliente)
        s.commit()
        s.refresh(cliente)
        return cliente
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def inserir_pedido(descricao: str, cliente_id: int) -> Pedido:
    s = get_session()
    try:
        # cliente_id é passado diretamente — o banco valida a FK automaticamente.
        # Se o cliente não existir, o banco lança um erro de integridade referencial.
        pedido = Pedido(descricao=descricao, cliente_id=cliente_id)
        s.add(pedido)
        s.commit()
        s.refresh(pedido)
        return pedido
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def listar_pedidos_por_cliente(cliente_id: int) -> tuple[Cliente | None, list[Pedido]]:
    s = get_session()
    try:
        cliente = s.query(Cliente).filter_by(id=cliente_id).first()
        if not cliente:
            return None, []
        # filter_by(cliente_id=...) gera WHERE cliente_id = :id — usa a FK para filtrar.
        pedidos = s.query(Pedido).filter_by(cliente_id=cliente_id).all()
        return cliente, pedidos
    finally:
        s.close()
