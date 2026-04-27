"""Sistema de Viagem no Tempo: alteracao de eventos e multiplas linhas do tempo."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

_db = os.path.join(os.path.dirname(__file__), "tempo.db")
if os.path.exists(_db):
    os.remove(_db)

from Controllers.tempo_controller import (
    inicializar, criar_viajante, criar_linha_tempo, criar_evento,
    viajar_no_tempo, listar_linhas_tempo, eventos_da_linha, historico_viajante,
)
from Views.tempo_view import exibir_todas_linhas, exibir_historico
from Models.base import session as db_session
from Models.viajante import Viajante

inicializar()

# Cria o viajante — o agente que irá alterar a história.
volta = criar_viajante("Volta ao Futuro", ano_base=2025)

# Cria a linha do tempo original com quatro eventos históricos.
lt_original = criar_linha_tempo("Linha Alpha", "A historia como conhecemos", original=True)

ev1 = criar_evento("Invencao da roda", -3500, lt_original.id)
ev2 = criar_evento("Queda do Imperio Romano", 476, lt_original.id)
ev3 = criar_evento("Invencao da internet", 1969, lt_original.id)
ev4 = criar_evento("Pandemia global de COVID-19", 2020, lt_original.id)

# Viagem 1: altera a queda de Roma — cria a Linha Beta onde Roma nunca caiu.
# A Linha Beta herda os eventos anteriores a 476 (só a invenção da roda) e substitui ev2.
viagem1, lt_beta = viajar_no_tempo(
    viajante_id=volta.id,
    evento_id=ev2.id,
    alteracao="O Imperio Romano nunca caiu, domina o mundo ate hoje",
    nome_nova_linha="Linha Beta (Roma Eterna)",
)
print(f"\n  Viagem 1 criou: {lt_beta.nome}")

# Viagem 2: altera a pandemia na linha original — cria a Linha Gamma sem COVID-19.
# A Linha Gamma herda todos os eventos até 2020 e substitui ev4.
viagem2, lt_gamma = viajar_no_tempo(
    viajante_id=volta.id,
    evento_id=ev4.id,
    alteracao="Vacina universal desenvolvida em 2019 - pandemia nunca aconteceu",
    nome_nova_linha="Linha Gamma (Sem Pandemia)",
)
print(f"  Viagem 2 criou: {lt_gamma.nome}")

# Carrega todas as linhas e seus eventos para exibição.
linhas = listar_linhas_tempo()
# Dict comprehension: {id_linha: [eventos]} — evita chamar eventos_da_linha N vezes na View.
eventos_por_linha = {lt.id: eventos_da_linha(lt.id) for lt in linhas}
exibir_todas_linhas(linhas, eventos_por_linha)

# Exibe o histórico de viagens do viajante.
# s.get() dentro de uma sessão própria para evitar erros de lazy loading fora de sessão.
s = db_session()
viajante_obj = s.get(Viajante, volta.id)
s.close()
exibir_historico(viajante_obj, historico_viajante(volta.id))
