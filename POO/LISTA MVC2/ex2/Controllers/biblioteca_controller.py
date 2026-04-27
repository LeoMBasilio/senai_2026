from datetime import datetime
from Models.base import Base, banco, session
from Models.usuario import Usuario
from Models.livro import Livro
from Models.emprestimo import Emprestimo


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


def cadastrar_livro(titulo: str, autor: str) -> Livro:
    s = session()
    try:
        l = Livro(titulo=titulo, autor=autor)
        s.add(l)
        s.commit()
        s.refresh(l)
        return l
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def pegar_emprestado(usuario_id: int, livro_id: int) -> Emprestimo:
    s = session()
    try:
        livro = s.get(Livro, livro_id)
        if livro is None:
            raise ValueError(f"Livro {livro_id} nao encontrado.")
        if not livro.disponivel:
            raise ValueError(f"Livro '{livro.titulo}' ja esta emprestado.")

        if s.get(Usuario, usuario_id) is None:
            raise ValueError(f"Usuario {usuario_id} nao encontrado.")

        livro.disponivel = False
        emp = Emprestimo(usuario_id=usuario_id, livro_id=livro_id)
        s.add(emp)
        s.commit()
        s.refresh(emp)
        return emp
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def devolver(emprestimo_id: int) -> Emprestimo:
    s = session()
    try:
        emp = s.get(Emprestimo, emprestimo_id)
        if emp is None:
            raise ValueError(f"Emprestimo {emprestimo_id} nao encontrado.")
        if not emp.ativo:
            raise ValueError("Este emprestimo ja foi encerrado.")

        emp.ativo = False
        emp.data_devolucao = datetime.now()
        livro = s.get(Livro, emp.livro_id)
        livro.disponivel = True
        s.commit()
        s.refresh(emp)
        return emp
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def listar_livros_disponiveis() -> list[Livro]:
    s = session()
    try:
        return s.query(Livro).filter(Livro.disponivel == True).all()
    finally:
        s.close()


def listar_emprestimos_ativos() -> list[Emprestimo]:
    s = session()
    try:
        return s.query(Emprestimo).filter(Emprestimo.ativo == True).all()
    finally:
        s.close()


def historico_usuario(usuario_id: int) -> list[Emprestimo]:
    s = session()
    try:
        return s.query(Emprestimo).filter(Emprestimo.usuario_id == usuario_id).all()
    finally:
        s.close()
