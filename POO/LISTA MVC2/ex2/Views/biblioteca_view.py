from Models.models import Livro, Emprestimo, Usuario


def exibir_livro(livro: Livro):
    status = "[OK] disponivel" if livro.disponivel else "[--] emprestado"
    print(f"  [{livro.id}] {livro.titulo} - {livro.autor} | {status}")


def exibir_livros_disponiveis(livros: list[Livro]):
    print("\n=== Livros Disponíveis ===")
    if not livros:
        print("  Nenhum livro disponível no momento.")
    for l in livros:
        exibir_livro(l)


def exibir_emprestimo(emp: Emprestimo):
    devolucao = emp.data_devolucao.strftime("%d/%m/%Y %H:%M") if emp.data_devolucao else "em aberto"
    print(
        f"  Empréstimo #{emp.id} | Livro: {emp.livro_id} | Usuário: {emp.usuario_id}"
        f" | Retirada: {emp.data_emprestimo.strftime('%d/%m/%Y %H:%M')}"
        f" | Devolução: {devolucao}"
    )


def exibir_emprestimos(emprestimos: list[Emprestimo], titulo: str = "Empréstimos"):
    print(f"\n=== {titulo} ===")
    if not emprestimos:
        print("  Nenhum empréstimo.")
    for emp in emprestimos:
        exibir_emprestimo(emp)


def exibir_devolucao(emp: Emprestimo):
    print(f"\n  Livro #{emp.livro_id} devolvido com sucesso! Empréstimo #{emp.id} encerrado.")
