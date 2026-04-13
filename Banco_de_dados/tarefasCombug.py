import sqlite3
from turtle import st

def Criar_tabela(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tarefas(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Titulo TEXT NOT NULL,
            Descricao TEXT,
            Status TEXT DEFAULT "Pendente"           
        );
    """)

def Selecionar_Tarefa(cursor, status=None):
    if type(status) != None or status.strip() != "":
        cursor.execute(f"""
            SELECT * FROM Tarefas WHERE Status = '{status}'
        """)
    else:
         cursor.execute("""
            SELECT * FROM Tarefas
        """)
    return cursor.fetchall()

def Update_Tarefas(cursor,id_tarefa, status=None, titulo=None, descricao=None):
    if type(id_tarefa) != None or id_tarefa.strip() != '':
        if type(status) != None:
            cursor.execute("""
                UPDATE Tarefas SET status = ?  WHERE ID = ?
            """, (status, id_tarefa))
        if type(titulo) != None:
            cursor.execute("""
                UPDATE Tarefas SET titulo = ? WHERE ID = ?
            """, (titulo, id_tarefa))
        if type(descricao) != None:
            cursor.execute("""
                UPDATE Tarefas SET descricao = ? WHERE ID = ?
            """, (descricao, id_tarefa))
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
            DELETE FROM Tarefa WHERE ID = {id_tarefa}
        """)
        return True
    return False

def main():
    conn = sqlite3.connect("Tarefas.db")
    cursor = conn.cursor()

    Criar_tabela(cursor)
    conn.commit()

    flag = True
    while flag:
        op = int(input("1.iserir\n2.listar\n3.atualizar\n4.deletar\n0.Sair\n\nEscolha: "))

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
                status = input("status: ") 
                status = None if type(status) == None or status.strip() == '' else status
                print(Selecionar_Tarefa(cursor, status))
            case 3:
                id_tarefa = input("Id: ")
                titulo = input("Titulo: ")
                descricao = input("Descricao: ")
                status = input("Status: ")

                if Update_Tarefas(cursor, id_tarefa, titulo, descricao, status):
                    conn.commit()
                    print("Deu bom")
                else:
                    print("deu ruim")
            case 4:
                id_tarefa = input("ID: ")

                if Deletar_tarefa(cursor, id_tarefa):
                    conn.commit()
                    print("Deu bom")
                else:
                    print("deu ruim")

            case 0:
                flag = False
            case _:
                print("Opção invalida")
            



if __name__ == "__main__":
    main()