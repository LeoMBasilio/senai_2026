import sqlite3

def criar_tabela(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano_publicacao INTEGER NOT NULL
        );
    ''')

def main():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    criar_tabela(cursor)

    opcao = input("1- Inserir\n 2-listar\n 3-Atualizar\nEscolha: ")

    match opcao:
        case "1":
            titulo = input("Título do livro: ")
            autor = input("Autor do livro: ")
            ano_publicacao = int(input("Ano de publicação: "))

            cursor.execute("""
                INSERT INTO livros (titulo, autor, ano_publicacao)
                VALUES (?, ?, ?);
            """, (titulo, autor, ano_publicacao))
            conn.commit()
        case "2":
            cursor.execute("SELECT * FROM livros;")
            livros = cursor.fetchall()
            for livro in livros:
                print(f"ID: {livro[0]} | Título: {livro[1]} | Autor: {livro[2]} | Ano de Publicação: {livro[3]}")

        case "3":
            id_livro = int(input("ID do livro a ser atualizado: "))
            opcao = input("1-TItulo\n 2-Autor\n 3-Ano de publicação\nEscolha: ")
            
            match opcao:
                case "1":
                    novo_titulo = input("Novo título do livro: ")
                    cursor.execute("""
                        UPDATE livros
                        SET titulo = ?
                        WHERE id = ?;
                    """, (novo_titulo, id_livro))
                    conn.commit()
                case "2":
                    novo_autor = input("Novo autor do livro: ")
                    cursor.execute("""
                        UPDATE livros
                        SET autor = ?
                        WHERE id = ?;
                    """, (novo_autor, id_livro))
                    conn.commit()

                case "3":
                    novo_ano_publicacao = int(input("Novo ano de publicação: "))
                    cursor.execute("""
                        UPDATE livros
                        SET ano_publicacao = ?
                        WHERE id = ?;
                    """, (novo_ano_publicacao, id_livro))
                    conn.commit()

                case _:
                    print("Opção inválida.")
                    return
if __name__ == "__main__":
    main()