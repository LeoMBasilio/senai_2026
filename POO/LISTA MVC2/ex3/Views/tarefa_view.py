from Models.models import Tarefa, Categoria


STATUS_ICONE = {
    "pendente": "[PEND]",
    "em_andamento": "[AND.]",
    "concluida": "[DONE]",
    "cancelada": "[CANC]",
}


def exibir_tarefa(t: Tarefa):
    icone = STATUS_ICONE.get(t.status.value, "?")
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
    print(f"  [{c.id}] {c.nome} — {c.descricao or 'sem descrição'}")


def exibir_categorias(categorias: list[Categoria]):
    print("\n=== Categorias ===")
    for c in categorias:
        exibir_categoria(c)


def exibir_atualizacao(t: Tarefa):
    print(f"\n  Tarefa #{t.id} '{t.titulo}' atualizada → {t.status.value}")
