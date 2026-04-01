import sqlite3
def main():
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Alunos(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL, 
            Idade INTEGER,
            Curso Text
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Notas(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            AlunoID INTEGER NOT NULL, 
            Nota INTEGER,
            Disciplina Text
        );
    """)

    conn.commit() # ! SEMPRE DEVE SER USADO APOS UMA ALTERAÇÃO

    opcao = int(input("escolha  "))

    match opcao:
        case 1:
            for _ in range(0, 5):
                nome = input("Nome: ")
                idade = int(input("Idade: "))
                curso = input("curso: ")

                cursor.execute("""
                    INSERT INTO Alunos(Nome, Idade, Curso) VALUES (?,?,?)
                """, (nome, idade, curso))

            conn.commit()
        
        case 2:
            cursor.execute("""
                SELECT * FROM Alunos    
            """)

            alunos = cursor.fetchall() #! TRAZ OS VALORES RECOLHIDOS NO SELECT

            for aluno in alunos:
                print(f"Nome:  {aluno[1]} | Idade: {aluno[2]} | Curso: {aluno[3]}")
        case 3:
            cursor.execute("""
                SELECT * FROM Alunos where Curso == "ti"
            """)

            alunos = cursor.fetchall()

            for aluno in alunos:
                print(f"Nome:  {aluno[1]} | Idade: {aluno[2]} | Curso: {aluno[3]}")

        case 4:
            alunoid = int(input("id do aluno: "))
            idade = int(input("Nova idade: "))

            cursor.execute("""
                UPDATE Alunos SET Idade = ? WHERE ID == ?
            """, (idade, alunoid))

            conn.commit()
        case 5:
            alunoid = int(input("id do aluno: "))

            cursor.execute(f"""
                DELETE FROM Alunos WHERE ID == {alunoid}
            """)

            conn.commit()

        case 6:
            cursor.execute("""
                SELECT Nome, Idade FROM Alunos where Idade > 20
            """)

            alunos = cursor.fetchall()

            for aluno in alunos:
                print(f"Nome:  {aluno[0]} | Idade: {aluno[1]}")
        case 6:
            cursor.execute("""
                SELECT Nome, Idade FROM Alunos where Idade > 20
            """)

            alunos = cursor.fetchall()

            for aluno in alunos:
                print(f"Nome:  {aluno[0]} | Idade: {aluno[1]}")
        case 7:
            cursor.execute("""
                SELECT Nome, Idade FROM Alunos where Nome LIKE 'J%'
            """)

            alunos = cursor.fetchall()

            for aluno in alunos:
                print(f"Nome:  {aluno[0]} | Idade: {aluno[1]}")
        case 8:
            cursor.execute("""
                SELECT Nome, Idade FROM Alunos ORDER BY Idade LIMIT 3
            """)

            alunos = cursor.fetchall()

            for aluno in alunos:
                print(f"Nome:  {aluno[0]} | Idade: {aluno[1]}")
        case 9:
            cursor.execute("""
                SELECT Nome, Idade FROM Alunos ORDER BY Nome DESC
            """)

            alunos = cursor.fetchall()

            for aluno in alunos:
                print(f"Nome:  {aluno[0]} | Idade: {aluno[1]}")

        case 10:
            alunoid = input("AlunoID: ")
            nota = int(input("Nota: "))
            disciplina = input("Disciplina: ")

            cursor.execute("""
                INSERT INTO Notas(AlunoID, Nota, Disciplina) VALUES (?,?,?)
            """, (alunoid, nota, disciplina))

            conn.commit()
        case 11:
            cursor.execute("""
                SELECT Alunos.Nome, Notas.Disciplina, Notas.Nota
                FROM Alunos
                INNER JOIN Notas ON Alunos.ID == Notas.AlunoID
            """)

            alunos = cursor.fetchall()

            for aluno in alunos:
                print(f"Nome:  {aluno[0]} | Nota: {aluno[2]} | Disciplina: {aluno[1]}")

if __name__ == "__main__":
    main()