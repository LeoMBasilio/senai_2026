# Models/status_crime.py — define o ciclo de vida de um crime usando Enum
# executar_crime() só aceita crimes PLANEJADOS — transições inválidas lançam ValueError.
# Em caso de sucesso → CONCLUIDO; em caso de falha → FALHOU.

import enum


class StatusCrime(enum.Enum):
    PLANEJADO = "planejado"        # crime registrado mas não iniciado
    EM_EXECUCAO = "em_execucao"    # crime em andamento (reservado para expansões futuras)
    CONCLUIDO = "concluido"        # crime bem-sucedido — vilão ganha poder_mundial
    FALHOU = "falhou"              # crime fracassado — vilão perde poder_mundial
