import sqlite3

def Criar_Tabela(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Produto(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Preco DECIMAL
        );
""")

def Exibir(cursor):
    cursor.execute("""
        SELECT * FROM Produto
    """)

    produtos = cursor.fetchall()

    for produto in produtos:
        print(f"ID: {produto[0]} | Nome: {produto[1]} | Preço: {produto[2]}")
def main():
    conn = sqlite3.connect("loja.db")
    cursor = conn.cursor()

    Criar_Tabela(cursor)
    conn.commit()

    opcao = input("1-Inserir\n 2-listar\n 3-Atualizar\nEscolha: ")

    match opcao:
        case "1":
            nome = input("nome do produto: ")
            preco = float(input("Preco do produto: "))

            cursor.execute("""
                INSERT INTO Produto(nome, preco) VALUES (?,?)
            """, (nome, preco))

            conn.commit()
        case "2":
            Exibir(cursor)

        case "3":
            opcao = input("1.nome\n2.Preco\nEscolha: ")

            match opcao:
                case '1':
                    id_prod = int(input("id: "))
                    nome = input("nome do produto: ")

                    cursor.execute("""
                        UPDATE Produto
                        SET nome = ?
                        WHERE id = ?;
                    """, (nome, id_prod))
                case '2':
                    id_prod = int(input("id: "))
                    preco = input("Preco do produto: ")

                    cursor.execute("""
                        UPDATE Produto
                        SET preco = ?
                        WHERE id = ?;
                    """, (preco, id_prod))

            conn.commit()
            Exibir(cursor)

if __name__ == "__main__":
    main()