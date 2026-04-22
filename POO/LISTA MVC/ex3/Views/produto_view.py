# Views/produto_view.py — camada de apresentação do ex3
# Cada função de exibição recebe o contexto da busca (termo, valor) para montar
# uma mensagem de cabeçalho informativa ao usuário.


def exibir_produto_criado(produto):
    print(f"[+] Produto criado: id={produto.id} | {produto.nome} | R${produto.preco:.2f} | estoque={produto.estoque}")


def exibir_busca(produtos, termo: str):
    # O termo é exibido no cabeçalho para o usuário saber qual filtro foi aplicado.
    print(f"\n--- Busca por '{termo}' ---")
    if not produtos:
        print("Nenhum produto encontrado.")
        return
    for p in produtos:
        print(f"  [{p.id}] {p.nome} — R${p.preco:.2f}")
    print(f"Encontrado(s): {len(produtos)}\n")


def exibir_filtro_preco(produtos, valor: float):
    print(f"\n--- Produtos com preço > R${valor:.2f} ---")
    if not produtos:
        print("Nenhum produto encontrado.")
        return
    for p in produtos:
        print(f"  [{p.id}] {p.nome} — R${p.preco:.2f}")
    print(f"Encontrado(s): {len(produtos)}\n")
