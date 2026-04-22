# Views/loja_view.py — camada de apresentação do ex4
# Exibe clientes e seus pedidos de forma legível. Não conhece SQL ou regras de negócio.


def exibir_cliente_criado(cliente):
    print(f"[+] Cliente criado: id={cliente.id} | {cliente.nome} | {cliente.email}")


def exibir_pedido_criado(pedido):
    print(f"[+] Pedido criado: id={pedido.id} | {pedido.descricao} | cliente_id={pedido.cliente_id}")


def exibir_pedidos_por_cliente(cliente, pedidos):
    if not cliente:
        print("[!] Cliente não encontrado.")
        return
    print(f"\n--- Pedidos de {cliente.nome} ---")
    if not pedidos:
        print("  Nenhum pedido encontrado.")
        return
    for p in pedidos:
        print(f"  [{p.id}] {p.descricao}")
    print(f"Total: {len(pedidos)} pedido(s)\n")
