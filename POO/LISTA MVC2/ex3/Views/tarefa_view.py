# Views/tarefa_view.py — camada de apresentação do ex3 (gerenciador de tarefas)
# Usa ícones para facilitar a leitura visual do status de cada tarefa.
# Nota: importa de Models.models (arquivo consolidado) — ver models.py do ex3.

from Models.models import Tarefa, Categoria


# Dicionário que mapeia o valor do Enum para um ícone de terminal.
# Usar um dict evita if/elif repetitivos para cada status.
STATUS_ICONE = {
    "pendente": "[PEND]",
    "em_andamento": "[AND.]",
    "concluida": "[DONE]",
    "cancelada": "[CANC]",
}


def exibir_tarefa(t: Tarefa):
    # .get() com fallback "?" evita KeyError se um novo status for adicionado sem atualizar o dict.
    icone = STATUS_ICONE.get(t.status.value, "?")
    # :<30 alinha o título à esquerda em 30 caracteres — mantém colunas alinhadas.
    print(f"  [{t.id}] {icone} {t.titulo:<30} | {t.status.value:<15} | Cat: {t.categoria_id}")
    if t.descricao:
        print(f"       {t.descricao}")


def exibir_lista_tarefas(tarefas: list[Tarefa], titulo: str = "Tarefas"):
    print(f"\n=== {titulo} ===")
    if not tarefas:
        print("  Nenhuma tarefa encontrada.")
    for t in tarefas:
        exibir_tarefa(t)


def exibir_categoria(c: Categoria):
    # "or 'sem descrição'" exibe um fallback quando a descrição é None ou vazia.
    print(f"  [{c.id}] {c.nome} — {c.descricao or 'sem descrição'}")


def exibir_categorias(categorias: list[Categoria]):
    print("\n=== Categorias ===")
    for c in categorias:
        exibir_categoria(c)


def exibir_atualizacao(t: Tarefa):
    print(f"\n  Tarefa #{t.id} '{t.titulo}' atualizada → {t.status.value}")
