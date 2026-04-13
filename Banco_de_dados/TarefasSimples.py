import sqlite3

def Criar_tabela(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tarefas(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Titulo TEXT NOT NULL,
            Descricao TEXT NOT NULL,
            Status TEXT
        )
    """)

def Selecionar_Todas_Tarefa(cursor):
    cursor.execute("""
        SELECT * FROM Tarefas
    """)
    return cursor.fetchall()

def Selecionar_Tarefa(cursor, status):
    cursor.execute(f"""
        SELECT * FROM Tarefas WHERE Status = '{status}'
    """)
    return cursor.fetchall()

def Update_Tarefas(cursor,id_tarefa, status, titulo, descricao):
    if type(id_tarefa) != None or id_tarefa.strip() != '':
        cursor.execute("""
            UPDATE Tarefas SET status = ?, titulo = ?, descricao = ? WHERE ID = ?
        """, (status, titulo, descricao, id_tarefa))
        return True
    return False

def Update_Tarefas_status(cursor,id_tarefa, status):
    if type(id_tarefa) != None or id_tarefa.strip() != '':
        cursor.execute("""
            UPDATE Tarefas SET status = ?  WHERE ID = ?
        """, (status, id_tarefa))
        return True
    return False

def Inserir_tarefas(cursor, titulo, descricao, status=None):
    if titulo.strip() != "":
        if status == None:
            cursor.execute("""
                INSERT INTO Tarefas(Titulo, Descricao) VALUES (?,?)
            """, (titulo, descricao))
        else:
            cursor.execute("""
                INSERT INTO Tarefas(Titulo, Descricao, Status) VALUES (?,?,?)
            """, (titulo, descricao, status))
        return True
    return False

def Deletar_tarefa(cursor, id_tarefa):
    if type(id_tarefa) != None:
        cursor.execute(f"""
            DELETE FROM Tarefas WHERE ID = {id_tarefa}
        """)
        return True
    return False

def main():
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()
    Criar_tabela(cursor)
    while True:
        print("1 - Inserir tarefa")
        print("2 - Listar tarefas")
        print("3 - Listar tarefas por status")
        print("4 - Atualizar tarefa")
        print("5 - Deletar tarefa")
        print("6 - Atualizar status da tarefa")
        print("0 - Sair")
        op = int(input("Opção: "))

        match op:
            case 1:
                titulo = input("Titulo: ")
                if type(titulo) == None or titulo.strip() == "":
                    print("Titulo é obrigatorio")
                    continue
                descricao = input("Descricao: ")
                status = input("Status: ") 
                if type(status) == None or status.strip() == "":
                    status = None
                
                if Inserir_tarefas(cursor, titulo, descricao, status):
                    conn.commit()
                    print("deu bom")
                else:
                    print("deu ruim")
            case 2:
                print(Selecionar_Todas_Tarefa(cursor))
            case 3:
                status = input("status: ") 
                status = None if type(status) == None or status.strip() == '' else status
                print(Selecionar_Tarefa(cursor, status))
            case 4:
                id_tarefa = input("Id: ")
                titulo = input("Titulo: ")
                descricao = input("Descricao: ")
                status = input("Status: ") 
                if type(status) == None or status.strip() == "":
                    status = None
                if Update_Tarefas(cursor, id_tarefa, status, titulo, descricao):
                    conn.commit()
                    print("deu bom")
                else:
                    print("deu ruim")
            case 5:
                id_tarefa = input("ID: ")
                if Deletar_tarefa(cursor, id_tarefa):
                    conn.commit()
                    print("deu bom")
                else:
                    print("deu ruim")

            case 6:
                id_tarefa = input("Id: ")
                status = input("Status: ") 
                if type(status) == None or status.strip() == "":
                    status = None
                if Update_Tarefas_status(cursor, id_tarefa, status):
                    conn.commit()
                    print("deu bom")
                else:
                    print("deu ruim")

            case 0:
                print("Saindo...")
                break
            case _:
                print("Opção invalida")
if __name__ == "__main__":
    main()