def exibir_usuario_criado(usuario):
    print(f"[+] Usuário criado: id={usuario.id} | {usuario.nome} | {usuario.email}")


def exibir_lista(usuarios):
    print("\n--- Lista de Usuários ---")
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    for u in usuarios:
        print(f"  [{u.id}] {u.nome} — {u.email}")
    print(f"Total: {len(usuarios)} usuário(s)\n")
