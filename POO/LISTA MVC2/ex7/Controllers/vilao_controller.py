# Controllers/vilao_controller.py — camada de lógica do ex7 (sistema de vilões)
# Mecânica de sucesso em executar_crime():
#   - Chance base: 70%
#   - Cada capanga adiciona +5% (até no máximo 95%)
#   - Sucesso: status CONCLUIDO, vilão ganha poder, domínio cresce.
#   - Falha: status FALHOU, vilão perde metade da recompensa em poder.

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
        # flush() obtém o id do vilão sem commitar — necessário para criar o DominioCriminal
        # na mesma transação usando o id recém-gerado.
        s.flush()
        # Todo vilão começa com um DominioCriminal padrão (Esconderijo Secreto).
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

        # Conta capangas do vilão — mais capangas = maior chance de sucesso.
        num_capangas = s.query(Capanga).filter(Capanga.vilao_id == crime.vilao_id).count()

        # Fórmula: 70% base + 5% por capanga, limitado a 95% (sempre há risco).
        sucesso = random.random() < min(0.95, 0.70 + num_capangas * 0.05)

        vilao = s.get(Vilao, crime.vilao_id)
        dominio = s.query(DominioCriminal).filter(DominioCriminal.vilao_id == crime.vilao_id).first()

        if sucesso:
            crime.status = StatusCrime.CONCLUIDO
            vilao.poder_mundial += crime.recompensa_poder
            if dominio:
                # Crimes bem-sucedidos expandem o domínio em 1.5x a recompensa de poder.
                dominio.pontos_dominio += crime.recompensa_poder * 1.5
        else:
            crime.status = StatusCrime.FALHOU
            # Penalidade: perde metade da recompensa, nunca abaixo de 0.
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
        # Conquista concede +50 pontos de domínio e +20 de poder mundial.
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
        # Ordena do mais poderoso para o menos — ranking decrescente.
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
