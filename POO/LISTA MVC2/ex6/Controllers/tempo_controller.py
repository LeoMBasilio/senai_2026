# Controllers/tempo_controller.py — camada de lógica do ex6 (viagem no tempo)
# A operação mais complexa é viajar_no_tempo():
#   1. Cria um registro de Viagem apontando para o evento a ser alterado.
#   2. Cria uma nova LinhaTempo divergente vinculada a essa viagem.
#   3. Copia para a nova linha todos os eventos anteriores ao alterado.
#   4. Adiciona o evento com a descrição modificada na nova linha.
# Resultado: a linha original permanece intacta; a nova linha tem o evento modificado.

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

        # Passo 1: registra a viagem — flush() obtém o id sem fazer commit ainda.
        viagem = Viagem(
            viajante_id=viajante_id,
            evento_id=evento_id,
            ano_destino=evento_original.ano,
            alteracao=alteracao,
        )
        s.add(viagem)
        s.flush()  # envia o INSERT ao banco mas mantém a transação aberta para usar viagem.id

        # Passo 2: cria a nova linha do tempo divergente vinculada a esta viagem.
        nova_lt = LinhaTempo(
            nome=nome_nova_linha,
            descricao=f"Divergencia da linha '{lt_original.nome}' em {evento_original.ano}",
            original=False,
            origem_viagem_id=viagem.id,
        )
        s.add(nova_lt)
        s.flush()  # obtém nova_lt.id para usar nos eventos abaixo

        # Passo 3: copia os eventos anteriores ao ponto de divergência para a nova linha.
        # Esses eventos são idênticos nas duas linhas — a divergência começa no evento alterado.
        eventos_anteriores = (
            s.query(Evento)
            .filter(
                Evento.linha_tempo_id == lt_original.id,
                Evento.ano <= evento_original.ano,
                Evento.id != evento_original.id,  # exclui o evento a ser substituído
            )
            .all()
        )
        for ev in eventos_anteriores:
            s.add(Evento(descricao=ev.descricao, ano=ev.ano, linha_tempo_id=nova_lt.id))

        # Passo 4: adiciona o evento alterado na nova linha com a nova descrição.
        # descricao_original preserva o texto anterior para comparação no relatório.
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
        # order_by(Evento.ano) ordena cronologicamente — mais legível na exibição.
        return s.query(Evento).filter(Evento.linha_tempo_id == linha_tempo_id).order_by(Evento.ano).all()
    finally:
        s.close()


def historico_viajante(viajante_id: int) -> list[Viagem]:
    s = session()
    try:
        return s.query(Viagem).filter(Viagem.viajante_id == viajante_id).all()
    finally:
        s.close()
