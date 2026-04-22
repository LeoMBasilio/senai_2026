# Views/produto_view.py — camada de apresentação do ex2
# Responsabilidade: apenas formatar e exibir dados. Nunca acessa o banco diretamente.
# Recebe objetos já prontos e decide como mostrá-los ao usuário.


def exibir_produto_criado(produto):
    # Acessa _preco diretamente porque o objeto vem do banco (já validado).
    print(f"[+] Produto criado: id={produto.id} | {produto.nome} | R${produto._preco:.2f} | estoque={produto._estoque}")


def exibir_produto_atualizado(produto):
    print(f"[~] Produto atualizado: id={produto.id} | {produto.nome} | R${produto._preco:.2f} | estoque={produto._estoque}")


def exibir_lista(produtos):
    print("\n--- Lista de Produtos ---")
    if not produtos:
        print("Nenhum produto cadastrado.")
        return
    for p in produtos:
        print(f"  [{p.id}] {p.nome} — R${p._preco:.2f} | estoque: {p._estoque}")
    print(f"Total: {len(produtos)} produto(s)\n")


def exibir_erro(mensagem: str):
    # Centraliza a formatação de erros para manter consistência visual.
    print(f"[ERRO] {mensagem}")
