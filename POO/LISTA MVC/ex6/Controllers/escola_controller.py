# Controllers/escola_controller.py — camada de lógica do ex6
# Gerencia matrículas e consultas do relacionamento N:N entre Aluno e Curso.

from Models.aluno import Aluno
from Models.curso import Curso
from Models.database import criar_tabelas, get_session


def inicializar():
    criar_tabelas()


def inserir_aluno(nome: str) -> Aluno:
    s = get_session()
    try:
        aluno = Aluno(nome=nome)
        s.add(aluno)
        s.commit()
        s.refresh(aluno)
        return aluno
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def inserir_curso(nome: str) -> Curso:
    s = get_session()
    try:
        curso = Curso(nome=nome)
        s.add(curso)
        s.commit()
        s.refresh(curso)
        return curso
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def matricular(aluno_id: int, curso_id: int):
    s = get_session()
    try:
        aluno = s.query(Aluno).filter_by(id=aluno_id).first()
        curso = s.query(Curso).filter_by(id=curso_id).first()
        if not aluno or not curso:
            raise ValueError("Aluno ou curso não encontrado.")
        # .append() no relationship com secondary faz o INSERT na tabela aluno_curso
        # automaticamente — sem precisar escrever SQL para a tabela de junção.
        aluno.cursos.append(curso)
        s.commit()
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def listar_cursos_do_aluno(aluno_id: int) -> tuple[Aluno | None, list[Curso]]:
    s = get_session()
    try:
        aluno = s.query(Aluno).filter_by(id=aluno_id).first()
        if not aluno:
            return None, []
        # list() força a leitura dos cursos enquanto a sessão ainda está aberta.
        # Sem isso, acessar aluno.cursos fora da sessão causaria um erro de lazy loading.
        return aluno, list(aluno.cursos)
    finally:
        s.close()


def listar_alunos_do_curso(curso_id: int) -> tuple[Curso | None, list[Aluno]]:
    s = get_session()
    try:
        curso = s.query(Curso).filter_by(id=curso_id).first()
        if not curso:
            return None, []
        return curso, list(curso.alunos)
    finally:
        s.close()
