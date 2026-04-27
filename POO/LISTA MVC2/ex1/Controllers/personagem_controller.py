from Models.base import Base, banco, session
from Models.personagem import Personagem
from Models.guerreiro import Guerreiro
from Models.mago import Mago
from Models.arqueiro import Arqueiro


def inicializar():
    Base.metadata.create_all(banco())


def criar_guerreiro(nome: str, nivel: int = 1, hp: int = 120, forca: int = 12) -> Guerreiro:
    s = session()
    try:
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
        return s.query(Personagem).all()
    finally:
        s.close()


def batalha(p1: Personagem, p2: Personagem) -> tuple:
    """Simula batalha alternada. Retorna (log_rodadas, vencedor, perdedor)."""
    p1.resetar_hp()
    p2.resetar_hp()
    rodadas = []
    turno = 0

    while p1.esta_vivo() and p2.esta_vivo():
        turno += 1
        atacante, defensor = (p1, p2) if turno % 2 != 0 else (p2, p1)

        resultado = atacante.atacar(defensor)
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

    s = session()
    try:
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
