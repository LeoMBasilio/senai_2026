# Controllers/personagem_controller.py — camada de lógica do ex1 (mini-RPG)
# Responsabilidade: criar personagens, persistir no banco e simular batalhas.
# O polimorfismo permite que batalha() funcione para qualquer combinação de classes
# sem precisar saber qual tipo cada combatente é.

from Models.base import Base, banco, session
from Models.personagem import Personagem
from Models.guerreiro import Guerreiro
from Models.mago import Mago
from Models.arqueiro import Arqueiro


def inicializar():
    # create_all cria todas as tabelas mapeadas pelo Base — neste caso só "personagens".
    Base.metadata.create_all(banco())


def criar_guerreiro(nome: str, nivel: int = 1, hp: int = 120, forca: int = 12) -> Guerreiro:
    s = session()
    try:
        # hp e hp_max recebem o mesmo valor inicial — hp_max serve para resetar antes de batalhas.
        p = Guerreiro(nome=nome, nivel=nivel, hp=hp, hp_max=hp, forca=forca)
        s.add(p)
        s.commit()
        s.refresh(p)
        return p
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def criar_mago(nome: str, nivel: int = 1, hp: int = 80, poder_magico: int = 10) -> Mago:
    s = session()
    try:
        p = Mago(nome=nome, nivel=nivel, hp=hp, hp_max=hp, poder_magico=poder_magico)
        s.add(p)
        s.commit()
        s.refresh(p)
        return p
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def criar_arqueiro(nome: str, nivel: int = 1, hp: int = 100, precisao: int = 9) -> Arqueiro:
    s = session()
    try:
        p = Arqueiro(nome=nome, nivel=nivel, hp=hp, hp_max=hp, precisao=precisao)
        s.add(p)
        s.commit()
        s.refresh(p)
        return p
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def listar_personagens() -> list[Personagem]:
    s = session()
    try:
        # O SQLAlchemy usa polymorphic_identity para instanciar o tipo correto
        # (Guerreiro, Mago ou Arqueiro) mesmo consultando a tabela base Personagem.
        return s.query(Personagem).all()
    finally:
        s.close()


def batalha(p1: Personagem, p2: Personagem) -> tuple:
    """Simula batalha alternada. Retorna (log_rodadas, vencedor, perdedor)."""
    # Reseta o hp antes de começar para não carregar dano de batalhas anteriores.
    p1.resetar_hp()
    p2.resetar_hp()
    rodadas = []
    turno = 0

    while p1.esta_vivo() and p2.esta_vivo():
        turno += 1
        # Rodadas ímpares: p1 ataca p2; Rodadas pares: p2 ataca p1.
        # Isso simula turnos alternados de combate.
        atacante, defensor = (p1, p2) if turno % 2 != 0 else (p2, p1)

        # Chama atacar() via polimorfismo — não importa se é Guerreiro, Mago ou Arqueiro.
        resultado = atacante.atacar(defensor)

        # Arqueiro retorna (dano, critico); outros retornam apenas int.
        # isinstance verifica o tipo em tempo de execução para tratar os dois casos.
        dano, critico = resultado if isinstance(resultado, tuple) else (resultado, False)

        rodadas.append({
            "rodada": turno,
            "atacante": atacante.nome,
            "defensor": defensor.nome,
            "dano": dano,
            "critico": critico,
            "hp_restante": defensor.hp,
        })

    vencedor = p1 if p1.esta_vivo() else p2
    perdedor = p2 if p1.esta_vivo() else p1

    # Persiste o hp final dos personagens no banco para refletir o estado após a batalha.
    s = session()
    try:
        # s.get() busca pelo id — mais eficiente que query().filter_by() para busca por PK.
        db_p1 = s.get(Personagem, p1.id)
        db_p2 = s.get(Personagem, p2.id)
        if db_p1:
            db_p1.hp = p1.hp
        if db_p2:
            db_p2.hp = p2.hp
        s.commit()
    finally:
        s.close()

    return rodadas, vencedor, perdedor
