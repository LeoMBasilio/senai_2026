import sqlite3

def Criar_Tabela(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cliente(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            email TEXT,
            ativo INTEGER NOT NULL
        )
    """)

def Exibir(cursor):
    cursor.execute("""
        SELECT * FROM Cliente
    """)

    Clientes = cursor.fetchall()

    for Cliente in Clientes:
        print(f"ID: {Cliente[0]} | Nome: {Cliente[1]} | email: {Cliente[2]}")

def main():
    conn = sqlite3.connect("Clientes.db")
    cursor = conn.cursor()

    Criar_Tabela(cursor)
    conn.commit()


    opcao = input("1-inserir\n2-listar\n3-delete\nEscolha: ")

    match opcao:
        case "1":
            nome = input("Nome: ")
            email = input("Email: ")
            status = int(input("Status: "))

            cursor.execute("""
                INSERT INTO Cliente(nome, email, ativo) VAlUES (?,?,?)
            """, (nome, email, status))
            conn.commit()
        case "2":
            Exibir(cursor)

        case "3":
            id_cliente = int(input("Id: "))

            cursor.execute(f"""
                DELETE FROM Cliente WHERE id = {id_cliente}
            """)
            conn.commit()
        case "4":
            cursor.execute(f"""
                DELETE FROM Cliente WHERE ativo = 0
            """)
            conn.commit()

if __name__ == "__main__":
    main()