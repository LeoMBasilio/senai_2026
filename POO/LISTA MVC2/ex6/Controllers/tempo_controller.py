from Models.base import Base, banco, session
from Models.viajante import Viajante
from Models.linha_tempo import LinhaTempo
from Models.evento import Evento
from Models.viagem import Viagem


def inicializar():
    Base.metadata.create_all(banco())


def criar_viajante(nome: str, ano_base: int = 2025) -> Viajante:
    s = session()
    try:
        v = Viajante(nome=nome, ano_base=ano_base)
        s.add(v)
        s.commit()
        s.refresh(v)
        return v
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def criar_linha_tempo(nome: str, descricao: str = "", original: bool = False) -> LinhaTempo:
    s = session()
    try:
        lt = LinhaTempo(nome=nome, descricao=descricao, original=original)
        s.add(lt)
        s.commit()
        s.refresh(lt)
        return lt
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def criar_evento(descricao: str, ano: int, linha_tempo_id: int) -> Evento:
    s = session()
    try:
        e = Evento(descricao=descricao, ano=ano, linha_tempo_id=linha_tempo_id)
        s.add(e)
        s.commit()
        s.refresh(e)
        return e
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def viajar_no_tempo(viajante_id: int, evento_id: int, alteracao: str, nome_nova_linha: str) -> tuple:
    """Altera um evento e gera uma nova linha do tempo divergente."""
    s = session()
    try:
        viajante = s.get(Viajante, viajante_id)
        if viajante is None:
            raise ValueError(f"Viajante {viajante_id} nao encontrado.")

        evento_original = s.get(Evento, evento_id)
        if evento_original is None:
            raise ValueError(f"Evento {evento_id} nao encontrado.")

        lt_original = s.get(LinhaTempo, evento_original.linha_tempo_id)

        viagem = Viagem(
            viajante_id=viajante_id,
            evento_id=evento_id,
            ano_destino=evento_original.ano,
            alteracao=alteracao,
        )
        s.add(viagem)
        s.flush()

        nova_lt = LinhaTempo(
            nome=nome_nova_linha,
            descricao=f"Divergencia da linha '{lt_original.nome}' em {evento_original.ano}",
            original=False,
            origem_viagem_id=viagem.id,
        )
        s.add(nova_lt)
        s.flush()

        eventos_anteriores = (
            s.query(Evento)
            .filter(
                Evento.linha_tempo_id == lt_original.id,
                Evento.ano <= evento_original.ano,
                Evento.id != evento_original.id,
            )
            .all()
        )
        for ev in eventos_anteriores:
            s.add(Evento(descricao=ev.descricao, ano=ev.ano, linha_tempo_id=nova_lt.id))

        s.add(Evento(
            descricao=alteracao,
            ano=evento_original.ano,
            alterado=True,
            descricao_original=evento_original.descricao,
            linha_tempo_id=nova_lt.id,
        ))

        s.commit()
        s.refresh(viagem)
        s.refresh(nova_lt)
        return viagem, nova_lt
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def listar_linhas_tempo() -> list[LinhaTempo]:
    s = session()
    try:
        return s.query(LinhaTempo).all()
    finally:
        s.close()


def eventos_da_linha(linha_tempo_id: int) -> list[Evento]:
    s = session()
    try:
        return s.query(Evento).filter(Evento.linha_tempo_id == linha_tempo_id).order_by(Evento.ano).all()
    finally:
        s.close()


def historico_viajante(viajante_id: int) -> list[Viagem]:
    s = session()
    try:
        return s.query(Viagem).filter(Viagem.viajante_id == viajante_id).all()
    finally:
        s.close()
