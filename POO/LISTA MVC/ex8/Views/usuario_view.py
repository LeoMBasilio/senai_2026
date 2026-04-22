# Views/usuario_view.py — camada de apresentação do ex8
# Recebe objetos Usuario e booleanos de resultado — sem dependência de banco.


def exibir_salvo(usuario):
    print(f"[+] Salvo: id={usuario.id} | {usuario.nome} | {usuario.email}")


def exibir_lista(usuarios):
    print("\n--- Lista de Usuários ---")
    if not usuarios:
        print("Nenhum usuário.")
        return
    for u in usuarios:
        print(f"  [{u.id}] {u.nome} — {u.email}")
    print(f"Total: {len(usuarios)}\n")


def exibir_busca(usuario, usuario_id: int):
    if usuario:
        print(f"[?] Encontrado: [{usuario.id}] {usuario.nome} | {usuario.email}")
    else:
        # Exibe o id buscado para deixar claro o que não foi encontrado.
        print(f"[!] Usuário id={usuario_id} não encontrado.")


def exibir_deletado(sucesso: bool, usuario_id: int):
    if sucesso:
        print(f"[-] Usuário id={usuario_id} deletado.")
    else:
        print(f"[!] Usuário id={usuario_id} não encontrado para deletar.")
