import enum


class StatusCrime(enum.Enum):
    PLANEJADO = "planejado"
    EM_EXECUCAO = "em_execucao"
    CONCLUIDO = "concluido"
    FALHOU = "falhou"
