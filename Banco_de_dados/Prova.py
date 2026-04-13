import sqlite3, os, platform

def limpar_tela():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def pausar():
    input("\n  Pressione ENTER para continuar...")

def cabecalho(titulo=""):
    limpar_tela()
    banner = [
        "  +================================================+",
        "  |   ____  _____  ___  ____  _   _ _____        |",
        "  |  / ___|  | | / _ |  _ | | | | | ____|       |",
        r"  |  \___ \ | | | | | | |_) | | | |  _|         |",
        "  |   ___) | | | | |_| |  _ <| |_| | |___        |",
        r"  |  |____/ |_|  \___/|_| \_\_____|_____|        |",
        "  |                                              |",
        "  |        Sistema de Controle de Estoque        |",
        "  +================================================+",
    ]
    print()
    for linha in banner:
        print(linha)
    if titulo:
        print(f"\n  {'─'*46}")
        print(f"   {titulo}")
        print(f"  {'─'*46}")

def conectar():
    return sqlite3.connect("estoque.db")

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Produtos (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            nome       TEXT    NOT NULL,
            quantidade INTEGER NOT NULL,
            preco      REAL    NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    

def inserir_produto():
    cabecalho("Adicionar Produto")
    nome = input("  Nome do produto: ").strip()
    nome = None if nome == "" else nome
    if nome is None:
        print("\n  [!] O nome do produto é obrigatório.")
        pausar()
        return
    
    try:
        quantidade = int(input("  Quantidade: "))
        preco = float(input("  Preço: R$ "))
    except ValueError:
        print("  [!] Quantidade e preco nao podem ser negativos.")
        pausar()
        return
    

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Produtos (nome, quantidade, preco) VALUES (?, ?, ?)", 
        (nome, quantidade, preco)
        )
    conn.commit()
    conn.close()

    print(f"\n  [OK] Produto '{nome}'adicionado com sucesso!")
    pausar()

def listar_produtos():
    cabecalho("Lista de Produtos")
    conn = conectar()
    cursor = conn.cursor()
    produtos = cursor.execute(
        "SELECT id, nome, quantidade, preco FROM Produtos ORDER BY nome"
    ).fetchall()
    conn.close()

    if not produtos:
        print("\n  Nenhum produto cadastrado.")
        pausar()
        return
    
    total_estoque = sum(q * p for _, _, q, p in produtos)

    print(f"\n  {'ID':<4} {'Nome':<20} {'Qtd':>5} {'Preço':>10} {'Total':>12}")
    print(f"  {'─'*54}")
    for id, nome, quantidade, preco in produtos:
        total_produto = quantidade * preco
        print(f"  {id:<4} {nome:<20} {quantidade:>5} R$ {preco:>9.2f} R$ {total_produto:>11.2f}")
    print(f"  {'─'*54}")
    print(f"  {'Valor total do estoque':>43} R$ {total_estoque:>9.2f}")
    pausar()

def atualizar_produto():
    cabecalho("Atualizar Produto")
    try:
        id = int(input("  ID do produto a atualizar: "))
    except ValueError:
        print("  [!] ID invalido.")
        pausar()
        return
    
    conn = conectar()
    cursor = conn.cursor()

    produto = cursor.execute(
        "SELECT id, nome, quantidade, preco FROM Produtos WHERE id = ?", (id,)
    ).fetchone()

    if not produto:
        print(f"  [!] Produto com ID {id} nao encontrado.")
        pausar()
        return
    
    _, nome, quantidade_atual, preco_atual = produto
    print(f"\n  Produto: {nome}")
    print(f"  Quantidade atual: {quantidade_atual}   |   Preço atual: R$ {preco_atual:.2f}")
    print("\n O que deseja atualizar?")
    print("  1. Quantidade")
    print("  2. Preço")
    print("  3. Ambos")
    opcao = input("\n  Opção: ").strip()
    nova_quantidade = quantidade_atual
    novo_preco = preco_atual

    try:
        if opcao in ("1", "3"):
            nova_quantidade = int(input("  Nova quantidade: "))
        if opcao in ("2", "3"):
            novo_preco = float(input("  Novo preço: R$ "))
    except ValueError:
        print("  [!] Quantidade e preço devem ser números válidos.")
        pausar()
        return
    
    cursor.execute(
        "UPDATE Produtos SET quantidade = ?, preco = ? WHERE id = ?", 
        (nova_quantidade, novo_preco, id)
    )
    conn.commit()
    conn.close()

    print(f"\n  [OK] Produto '{nome}' atualizado com sucesso!")
    pausar()

def remover_produto():
    cabecalho("Remover Produto")
    try:
        id = int(input("  ID do produto a remover: "))
    except ValueError:
        print("  [!] ID invalido.")
        pausar()
        return
    
    conn = conectar()
    cursor = conn.cursor()

    produto = cursor.execute(
        "SELECT id, nome FROM Produtos WHERE id = ?", (id,)
    ).fetchone()

    if not produto:
        print(f"  [!] Produto com ID {id} nao encontrado.")
        pausar()
        return
    
    _, nome = produto
    confirmacao = input(f"  Tem certeza que deseja remover o produto '{nome}'? (s/n): ").strip().lower()
    if confirmacao != 's':
        print("  Operação cancelada.")
        pausar()
        return
    
    cursor.execute("DELETE FROM Produtos WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    print(f"\n  [OK] Produto '{nome}' removido com sucesso!")
    pausar()

def Buscar_produto():
    cabecalho("Buscar Produto")
    print("\n  [1] Buscar por ID")
    print("\n [2] Buscar por nome")
    opcao = input("\n  Opção: ").strip()
    conn = conectar()
    cursor = conn.cursor()

    if opcao == "1":
        try:
            id = int(input("  ID: "))
        except ValueError:
            print("  [!] ID invalido.")
            pausar()
            return
        produtos = cursor.execute(
            "SELECT id, nome, quantidade, preco FROM Produtos WHERE id = ?", (id,)
        ).fechoneall()
    elif opcao == "2":
        nome = input("  Nome (parcial): ").strip()
        produtos = cursor.execute(
            "SELECT id, nome, quantidade, preco FROM Produtos WHERE nome LIKE ?", 
            (f"%{nome}%",)
        ).fetchall()
    else:
        print("  [!] Opção invalida.")
        pausar()
        return
    
    conn.close()

    if not produtos:
        print("\n  Nenhum produto encontrado.")
        pausar()
        return
    else:
        print(f"\n  {'ID':<4} {'Nome':<20} {'Qtd':>5} {'Preço':>10}")
        print(f"  {'─'*43}")
        for id, nome, quantidade, preco in produtos:
            print(f"  {id:<4} {nome:<20} {quantidade:>5} R$ {preco:>9.2f}")
        pausar()

def menu():
    criar_tabela()
    while True:
        cabecalho("Menu Principal")
        print("""
  +--------------------------------------+
  |           MENU PRINCIPAL             |
  +--------------------------------------+
  |  [1]  Adicionar Produto              |
  |  [2]  Listar Produtos                |
  |  [3]  Atualizar Produto              |
  |  [4]  Remover Produto                |
  |  [5]  Buscar Produto                 |
  |  [0]  Sair                           |
  +--------------------------------------+""")

        opcao = input("\n  Opção: ").strip()

        if opcao == "1":
            inserir_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            atualizar_produto()
        elif opcao == "4":
            remover_produto()
        elif opcao == "5":
            Buscar_produto()
        elif opcao == "0":
            print("\n  Saindo do sistema...")
            break
        else:
            print("  [!] Opção invalida.")
            pausar()

if __name__ == "__main__":
    menu()
