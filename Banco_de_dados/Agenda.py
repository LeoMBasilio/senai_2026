import sqlite3
def Conectar():
    return sqlite3.connect("agenda.db")

def Criar_tabela():
    conn = Conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Agenda(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Telefone INTEGER,
            Email TEXT
            );
    """)

    conn.commit()
    conn.close()

def Inserir_Contato(nome, telefone, email):
    conn = Conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Agenda(nome, telefone, email) VALUES (?,?,?)
        """, (nome, telefone, email))
    except:
        conn.close()
        return False

    conn.commit()
    conn.close()
    return True

def Update_Contato(id_contato, nome=None, telefone=None, email=None):
    conn = Conectar()
    cursor = conn.cursor()
    if type(id_contato) != None:
        if type(nome) != None:
            cursor.execute("""
                UPDATE Agenda SET Nome = ? WHERE id = ?
            """, (nome, id_contato))
        if telefone != None:
            cursor.execute("""
                UPDATE Agenda SET Telefone = ? WHERE id = ?
            """, (telefone, id_contato))
        if email != None:
            cursor.execute("""
                UPDATE Agenda SET Email = ? WHERE id = ?
            """, (email, id_contato))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def Deletar_Contato(id_contato):
    conn = Conectar()
    cursor = conn.cursor()

    if (type(id_contato) != None) and (id_contato.strip() != ''):
        cursor.execute(f"""
            DELETE FROM Agenda WHERE ID == {id_contato}
        """)
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def Selecionar_Contato(id_contato=None, nome=None):
    conn = Conectar()
    cursor = conn.cursor()

    if (type(id_contato) != None) and (type(nome) != None):
        cursor.execute("""
            SELECT * FROM Agenda
        """)
        result = cursor.fetchall()
        conn.close()
        return result
    elif type(nome) != None:
        cursor.execute("""
            SELECT * FROM Agenda WHERE nome = ?
        """, (nome))
        result = cursor.fetchall()
        conn.close()
        return result
    else:
        cursor.execute("""
            SELECT * FROM Agenda WHERE ID = ?
        """, (id_contato))
        result = cursor.fetchall()
        conn.close()
        return result

def main():
    op = int(input("1.iserir\n2.listar\n3.atualizar\n4.deletar\nEscolha: "))

    match op:
        case 1:
            nome = input("Nome: ")
            telefone = int(input("Telefone: "))
            email = input("Email: ")

            if Inserir_Contato(nome, telefone, email):
                print("Dados Inseridos")
            else:
                print("Erro ao inserir")
        case 2:
            print(Selecionar_Contato())
        case 3:
            id_contato = int(input("ID: "))

            op = int(input("1. Nome\n2.Telefone\n3.Email\nEscolha: "))

            match op:
                case 1:
                    nome = input("Nome: ")
                    if Update_Contato(id_contato, nome):
                        print("Deu certo")
                    else:
                        print("Deu ruim")
                case 2:
                    telefone = input("Telefone: ")
                    if Update_Contato(id_contato, telefone):
                        print("Deu certo")
                    else:
                        print("Deu ruim")
                case 1:
                    email = input("Email: ")
                    if Update_Contato(id_contato, email):
                        print("Deu certo")
                    else:
                        print("Deu ruim")
        case 4:
            id_contato = int(input("Qual usuario quer deletar\nID:"))
            if Deletar_Contato(id_contato):
                print("deu Bom")
            else:
                print("deu ruim")

if __name__ == "__main__":
    main()