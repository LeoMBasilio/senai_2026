# Controllers/tarefa_controller.py — camada de lógica do ex3 (gerenciador de tarefas)
# Gerencia criação de usuários, categorias e tarefas, além de filtragem por status e categoria.

from Models.base import Base, banco, session
from Models.usuario import Usuario
from Models.categoria import Categoria
from Models.tarefa import Tarefa
from Models.status_tarefa import StatusTarefa


def inicializar():
    Base.metadata.create_all(banco())


def criar_usuario(nome: str) -> Usuario:
    s = session()
    try:
        u = Usuario(nome=nome)
        s.add(u)
        s.commit()
        s.refresh(u)
        return u
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def criar_categoria(nome: str, descricao: str = "") -> Categoria:
    s = session()
    try:
        c = Categoria(nome=nome, descricao=descricao)
        s.add(c)
        s.commit()
        s.refresh(c)
        return c
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def criar_tarefa(titulo: str, descricao: str, usuario_id: int, categoria_id: int) -> Tarefa:
    s = session()
    try:
        # O status começa como PENDENTE por padrão (definido na Model).
        t = Tarefa(titulo=titulo, descricao=descricao, usuario_id=usuario_id, categoria_id=categoria_id)
        s.add(t)
        s.commit()
        s.refresh(t)
        return t
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def atualizar_status(tarefa_id: int, novo_status: StatusTarefa) -> Tarefa:
    s = session()
    try:
        t = s.get(Tarefa, tarefa_id)
        if t is None:
            raise ValueError(f"Tarefa {tarefa_id} nao encontrada.")
        # Atribuir um membro do Enum garante que só valores válidos entrem no banco.
        t.status = novo_status
        s.commit()
        s.refresh(t)
        return t
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def listar_por_categoria(categoria_id: int) -> list[Tarefa]:
    s = session()
    try:
        # Filtra pela FK categoria_id — retorna tarefas independente do status.
        return s.query(Tarefa).filter(Tarefa.categoria_id == categoria_id).all()
    finally:
        s.close()


def listar_por_status(status: StatusTarefa) -> list[Tarefa]:
    s = session()
    try:
        # Filtra pelo valor do Enum — o SQLAlchemy converte para a string do .value.
        return s.query(Tarefa).filter(Tarefa.status == status).all()
    finally:
        s.close()


def listar_tarefas_usuario(usuario_id: int) -> list[Tarefa]:
    s = session()
    try:
        return s.query(Tarefa).filter(Tarefa.usuario_id == usuario_id).all()
    finally:
        s.close()


def listar_categorias() -> list[Categoria]:
    s = session()
    try:
        return s.query(Categoria).all()
    finally:
        s.close()
