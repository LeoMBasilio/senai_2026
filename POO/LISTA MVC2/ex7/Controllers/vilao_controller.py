import random
from datetime import datetime
from Models.base import Base, banco, session
from Models.vilao import Vilao
from Models.capanga import Capanga
from Models.crime import Crime
from Models.dominio_criminal import DominioCriminal
from Models.status_crime import StatusCrime


def inicializar():
    Base.metadata.create_all(banco())


def criar_vilao(nome: str, codinome: str = "") -> Vilao:
    s = session()
    try:
        v = Vilao(nome=nome, codinome=codinome)
        s.add(v)
        s.flush()
        s.add(DominioCriminal(vilao_id=v.id))
        s.commit()
        s.refresh(v)
        return v
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def contratar_capanga(vilao_id: int, nome: str, habilidade: str) -> Capanga:
    s = session()
    try:
        if s.get(Vilao, vilao_id) is None:
            raise ValueError(f"Vilao {vilao_id} nao encontrado.")
        c = Capanga(nome=nome, habilidade=habilidade, vilao_id=vilao_id)
        s.add(c)
        s.commit()
        s.refresh(c)
        return c
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def planejar_crime(vilao_id: int, nome: str, descricao: str, recompensa_poder: int) -> Crime:
    s = session()
    try:
        crime = Crime(nome=nome, descricao=descricao, recompensa_poder=recompensa_poder, vilao_id=vilao_id)
        s.add(crime)
        s.commit()
        s.refresh(crime)
        return crime
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def executar_crime(crime_id: int) -> tuple[Crime, bool]:
    s = session()
    try:
        crime = s.get(Crime, crime_id)
        if crime is None:
            raise ValueError(f"Crime {crime_id} nao encontrado.")
        if crime.status != StatusCrime.PLANEJADO:
            raise ValueError("So e possivel executar crimes planejados.")

        num_capangas = s.query(Capanga).filter(Capanga.vilao_id == crime.vilao_id).count()
        sucesso = random.random() < min(0.95, 0.70 + num_capangas * 0.05)

        vilao = s.get(Vilao, crime.vilao_id)
        dominio = s.query(DominioCriminal).filter(DominioCriminal.vilao_id == crime.vilao_id).first()

        if sucesso:
            crime.status = StatusCrime.CONCLUIDO
            vilao.poder_mundial += crime.recompensa_poder
            if dominio:
                dominio.pontos_dominio += crime.recompensa_poder * 1.5
        else:
            crime.status = StatusCrime.FALHOU
            vilao.poder_mundial = max(0, vilao.poder_mundial - crime.recompensa_poder // 2)

        crime.executado_em = datetime.now()
        s.commit()
        s.refresh(crime)
        return crime, sucesso
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def conquistar_territorio(vilao_id: int, territorio: str):
    s = session()
    try:
        dominio = s.query(DominioCriminal).filter(DominioCriminal.vilao_id == vilao_id).first()
        if dominio is None:
            raise ValueError("Vilao sem dominio registrado.")
        dominio.territorio = territorio
        dominio.pontos_dominio += 50
        vilao = s.get(Vilao, vilao_id)
        vilao.poder_mundial += 20
        s.commit()
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def ranking_viloes() -> list[Vilao]:
    s = session()
    try:
        return s.query(Vilao).order_by(Vilao.poder_mundial.desc()).all()
    finally:
        s.close()


def buscar_vilao(vilao_id: int) -> Vilao:
    s = session()
    try:
        return s.get(Vilao, vilao_id)
    finally:
        s.close()


def listar_capangas(vilao_id: int) -> list[Capanga]:
    s = session()
    try:
        return s.query(Capanga).filter(Capanga.vilao_id == vilao_id).all()
    finally:
        s.close()


def listar_crimes(vilao_id: int) -> list[Crime]:
    s = session()
    try:
        return s.query(Crime).filter(Crime.vilao_id == vilao_id).all()
    finally:
        s.close()
