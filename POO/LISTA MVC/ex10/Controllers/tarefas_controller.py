# Controllers/tarefas_controller.py — camada de lógica do ex10
# CRUD completo para Usuario e Tarefa.
# Funções separadas por entidade mas no mesmo arquivo, pois as duas estão fortemente ligadas.

from Models.usuario import Usuario
from Models.tarefa import Tarefa
from Models.database import criar_tabelas, get_session


def inicializar():
    criar_tabelas()


# ─── CRUD Usuario ────────────────────────────────────────────────────────────

def criar_usuario(nome: str, email: str) -> Usuario:
    s = get_session()
    try:
        usuario = Usuario(nome=nome, email=email)
        s.add(usuario)
        s.commit()
        s.refresh(usuario)
        return usuario
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def listar_usuarios() -> list[Usuario]:
    s = get_session()
    try:
        return s.query(Usuario).all()
    finally:
        s.close()


def buscar_usuario(usuario_id: int) -> Usuario | None:
    s = get_session()
    try:
        return s.query(Usuario).filter_by(id=usuario_id).first()
    finally:
        s.close()


def atualizar_usuario(usuario_id: int, nome: str | None = None, email: str | None = None) -> Usuario:
    s = get_session()
    try:
        usuario = s.query(Usuario).filter_by(id=usuario_id).first()
        if not usuario:
            raise ValueError(f"Usuário {usuario_id} não encontrado.")
        # Atualiza apenas os campos fornecidos — None significa "não alterar".
        if nome:
            usuario.nome = nome
        if email:
            usuario.email = email
        s.commit()
        s.refresh(usuario)
        return usuario
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def deletar_usuario(usuario_id: int) -> bool:
    s = get_session()
    try:
        usuario = s.query(Usuario).filter_by(id=usuario_id).first()
        if not usuario:
            return False
        # cascade="all, delete-orphan" no modelo garante que as tarefas
        # do usuário são deletadas junto, sem precisar de lógica extra aqui.
        s.delete(usuario)
        s.commit()
        return True
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


# ─── CRUD Tarefa ─────────────────────────────────────────────────────────────

def criar_tarefa(titulo: str, usuario_id: int) -> Tarefa:
    s = get_session()
    try:
        tarefa = Tarefa(titulo=titulo, usuario_id=usuario_id)
        s.add(tarefa)
        s.commit()
        s.refresh(tarefa)
        return tarefa
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def listar_tarefas_do_usuario(usuario_id: int) -> list[Tarefa]:
    s = get_session()
    try:
        return s.query(Tarefa).filter_by(usuario_id=usuario_id).all()
    finally:
        s.close()


def concluir_tarefa(tarefa_id: int) -> Tarefa:
    s = get_session()
    try:
        tarefa = s.query(Tarefa).filter_by(id=tarefa_id).first()
        if not tarefa:
            raise ValueError(f"Tarefa {tarefa_id} não encontrada.")
        tarefa.concluida = True  # altera o campo booleano — o commit persiste a mudança
        s.commit()
        s.refresh(tarefa)
        return tarefa
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def atualizar_tarefa(tarefa_id: int, titulo: str) -> Tarefa:
    s = get_session()
    try:
        tarefa = s.query(Tarefa).filter_by(id=tarefa_id).first()
        if not tarefa:
            raise ValueError(f"Tarefa {tarefa_id} não encontrada.")
        tarefa.titulo = titulo
        s.commit()
        s.refresh(tarefa)
        return tarefa
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def deletar_tarefa(tarefa_id: int) -> bool:
    s = get_session()
    try:
        tarefa = s.query(Tarefa).filter_by(id=tarefa_id).first()
        if not tarefa:
            return False
        s.delete(tarefa)
        s.commit()
        return True
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()
