# Views/pedido_view.py — camada de apresentação do ex5
# Formata os dados do pedido com itens e total final de forma legível.


def exibir_produto_criado(produto):
    print(f"[+] Produto: id={produto.id} | {produto.nome} | R${produto.preco:.2f}")


def exibir_pedido(pedido, itens, total):
    print(f"\n--- Pedido #{pedido.id} ---")
    for item in itens:
        subtotal = item.quantidade * item.preco_unitario
        # Exibe cada linha do pedido com subtotal calculado na view (só formatação).
        print(f"  Produto id={item.produto_id} | qty={item.quantidade} | unit=R${item.preco_unitario:.2f} | subtotal=R${subtotal:.2f}")
    print(f"  TOTAL: R${total:.2f}\n")
