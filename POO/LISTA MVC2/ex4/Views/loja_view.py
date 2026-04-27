# Views/loja_view.py — camada de apresentação do ex4 (loja e-commerce)
# Exibe catálogo, itens de pedido e lista de pedidos formatados.
# Importa de Models.models (arquivo consolidado) — ver models.py do ex4.

from Models.models import Produto, Pedido, ItemPedido


def exibir_produto(p: Produto):
    # :<30 e :>8 alinham colunas — deixam o catálogo visualmente organizado.
    print(f"  [{p.id}] {p.nome:<30} | R$ {p.preco:>8.2f} | Estoque: {p.estoque}")


def exibir_catalogo(produtos: list[Produto]):
    print("\n=== Catálogo de Produtos ===")
    print(f"  {'ID':<4} {'Nome':<30} {'Preço':>10} {'Estoque':>8}")
    print("  " + "-" * 56)
    if not produtos:
        print("  Nenhum produto disponível.")
    for p in produtos:
        exibir_produto(p)


def exibir_item(item: ItemPedido):
    # Exibe quantidade, produto, preço unitário e subtotal por linha.
    print(f"    - {item.quantidade}x item #{item.produto_id} @ R${item.preco_unitario:.2f} = R${item.subtotal:.2f}")


def exibir_pedido(pedido: Pedido):
    print(f"\n  Pedido #{pedido.id} | Status: {pedido.status.value} | Total: R${pedido.total:.2f}")
    for item in pedido.itens:
        exibir_item(item)


def exibir_pedidos(pedidos: list[Pedido], titulo: str = "Pedidos"):
    print(f"\n=== {titulo} ===")
    if not pedidos:
        print("  Nenhum pedido encontrado.")
    for p in pedidos:
        exibir_pedido(p)
