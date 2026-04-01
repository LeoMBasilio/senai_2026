import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Cliente(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nome TEXT NOT NULL,
        Email TEXT
        );
    """)

    cursor.execute("""
         CREATE TABLE IF NOT EXISTS Produto(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nome TEXT NOT NULL,
        Preco DECIMAL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Pedido (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ClienteID INTEGER,
            ProdutoID INTEGER,
            Quantidade INTEGER,
            Data DATE,
            FOREIGN KEY (ClienteID) REFERENCES Cliente(ID),
            FOREIGN KEY (ProdutoID) REFERENCES Produto(ID)
            );
    """)

    conn.commit()
    
    try:
        cursor.execute("""
            ALTER TABLE Cliente 
            ADD telefone INTEGER(11)
        """)

        conn.commit()
    except:
        pass

    cursor.execute("""
        SELECT nome FROM Cliente
    """)

    filtro = cursor.fetchall()
    for i in filtro:
        for j in i:
            if j != "Joana":
                print(type(j))
                cursor.execute("""
                    INSERT INTO Cliente(Nome,Email)
                    VALUES (?,?)
                """, ("Joana", "Joana@email.com"))

                conn.commit()

    conn.close()