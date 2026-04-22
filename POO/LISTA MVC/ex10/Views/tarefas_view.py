# Views/tarefas_view.py — camada de apresentação do ex10
# Formata usuários e tarefas para o terminal. Recebe objetos prontos, nunca acessa banco.


def exibir_usuario(usuario, acao="criado"):
    print(f"[+] Usuário {acao}: id={usuario.id} | {usuario.nome} | {usuario.email}")


def exibir_lista_usuarios(usuarios):
    print("\n--- Usuários ---")
    if not usuarios:
        print("Nenhum usuário.")
        return
    for u in usuarios:
        print(f"  [{u.id}] {u.nome} — {u.email}")
    print()


def exibir_tarefa(tarefa, acao="criada"):
    status = "concluída" if tarefa.concluida else "pendente"
    print(f"[+] Tarefa {acao}: id={tarefa.id} | {tarefa.titulo} | {status}")


def exibir_tarefas(tarefas, usuario_nome: str):
    print(f"\n--- Tarefas de {usuario_nome} ---")
    if not tarefas:
        print("  Nenhuma tarefa.")
        return
    for t in tarefas:
        # [✓] para concluída e [ ] para pendente — facilita leitura visual.
        status = "[✓]" if t.concluida else "[ ]"
        print(f"  {status} [{t.id}] {t.titulo}")
    print()


def exibir_deletado(sucesso: bool, tipo: str, item_id: int):
    if sucesso:
        print(f"[-] {tipo} id={item_id} deletado(a).")
    else:
        print(f"[!] {tipo} id={item_id} não encontrado(a).")
