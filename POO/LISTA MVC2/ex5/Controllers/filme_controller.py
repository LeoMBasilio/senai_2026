# Controllers/filme_controller.py — camada de lógica do ex5 (avaliação de filmes)
# Responsabilidade: gerenciar filmes, avaliações e cálculo de médias/rankings.
# Regras importantes:
#   - Um usuário só pode ter UMA avaliação por filme (atualiza se já existir).
#   - Nota deve estar entre 0 e 10.

from sqlalchemy import func
from Models.base import Base, banco, session
from Models.usuario import Usuario
from Models.filme import Filme
from Models.avaliacao import Avaliacao


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


def cadastrar_filme(titulo: str, ano: int, genero: str = "", diretor: str = "") -> Filme:
    s = session()
    try:
        f = Filme(titulo=titulo, ano=ano, genero=genero, diretor=diretor)
        s.add(f)
        s.commit()
        s.refresh(f)
        return f
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def avaliar(usuario_id: int, filme_id: int, nota: float, comentario: str = "") -> Avaliacao:
    # Valida a nota antes de abrir a sessão — evita operação no banco com valor inválido.
    if not 0 <= nota <= 10:
        raise ValueError("Nota deve ser entre 0 e 10.")
    s = session()
    try:
        # Busca se o usuário já avaliou este filme — regra: uma avaliação por filme por usuário.
        existente = (
            s.query(Avaliacao)
            .filter(Avaliacao.usuario_id == usuario_id, Avaliacao.filme_id == filme_id)
            .first()
        )
        if existente:
            # Atualiza a avaliação existente em vez de criar uma duplicata.
            existente.nota = nota
            existente.comentario = comentario
            s.commit()
            s.refresh(existente)
            return existente

        av = Avaliacao(usuario_id=usuario_id, filme_id=filme_id, nota=nota, comentario=comentario)
        s.add(av)
        s.commit()
        s.refresh(av)
        return av
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def media_notas(filme_id: int) -> float | None:
    s = session()
    try:
        # func.avg() delega o cálculo da média ao banco — mais eficiente que carregar todos os registros.
        # .scalar() retorna o único valor da query (o resultado do AVG).
        resultado = (
            s.query(func.avg(Avaliacao.nota))
            .filter(Avaliacao.filme_id == filme_id)
            .scalar()
        )
        # round(..., 2) limita a 2 casas decimais para exibição.
        return round(resultado, 2) if resultado is not None else None
    finally:
        s.close()


def listar_avaliacoes_filme(filme_id: int) -> list[Avaliacao]:
    s = session()
    try:
        return s.query(Avaliacao).filter(Avaliacao.filme_id == filme_id).all()
    finally:
        s.close()


def listar_filmes() -> list[Filme]:
    s = session()
    try:
        return s.query(Filme).all()
    finally:
        s.close()


def ranking_filmes() -> list[tuple]:
    s = session()
    try:
        # outerjoin inclui filmes sem avaliações (média = None) na lista.
        # group_by agrupa por filme para calcular a média de cada um.
        # order_by ... desc() ordena do melhor para o pior.
        return (
            s.query(Filme, func.avg(Avaliacao.nota).label("media"), func.count(Avaliacao.id).label("total"))
            .outerjoin(Avaliacao, Filme.id == Avaliacao.filme_id)
            .group_by(Filme.id)
            .order_by(func.avg(Avaliacao.nota).desc())
            .all()
        )
    finally:
        s.close()
