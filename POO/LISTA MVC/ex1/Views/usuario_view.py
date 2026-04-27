# Views/usuario_view.py — camada de apresentação do ex1
# Responsabilidade: formatar e exibir dados para o usuário.
# A View NUNCA acessa o banco diretamente — recebe objetos prontos e decide como mostrá-los.
# Separar a apresentação da lógica facilita mudar o visual sem mexer nas regras de negócio.


def exibir_usuario_criado(usuario):
    # Recebe um objeto Usuario e imprime uma confirmação de criação com seus dados.
    print(f"[+] Usuário criado: id={usuario.id} | {usuario.nome} | {usuario.email}")


def exibir_lista(usuarios):
    print("\n--- Lista de Usuários ---")
    # Verifica se a lista está vazia antes de iterar — evita imprimir cabeçalho vazio.
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    for u in usuarios:
        print(f"  [{u.id}] {u.nome} — {u.email}")
    # len() conta quantos objetos há na lista — útil para confirmar quantos registros existem.
    print(f"Total: {len(usuarios)} usuário(s)\n")
