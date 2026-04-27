# Models/status_tarefa.py — define os estados possíveis de uma tarefa usando Enum
# Enum (enumeração) garante que o campo "status" só aceite valores predefinidos.
# Isso evita strings inválidas como "concluiido" ou "DONE" sendo gravadas no banco.
# O SQLAlchemy armazena o .value (a string) no banco, não o nome do membro Python.

import enum


class StatusTarefa(enum.Enum):
    PENDENTE = "pendente"          # tarefa criada mas ainda não iniciada
    EM_ANDAMENTO = "em_andamento"  # tarefa em progresso
    CONCLUIDA = "concluida"        # tarefa finalizada com sucesso
    CANCELADA = "cancelada"        # tarefa abandonada
