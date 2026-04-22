# Views/escola_view.py — camada de apresentação do ex6
# Exibe alunos, cursos e matrículas. Não conhece a tabela de junção.


def exibir_aluno_criado(aluno):
    print(f"[+] Aluno: id={aluno.id} | {aluno.nome}")


def exibir_curso_criado(curso):
    print(f"[+] Curso: id={curso.id} | {curso.nome}")


def exibir_matricula(aluno_id, curso_id):
    print(f"[~] Aluno {aluno_id} matriculado no curso {curso_id}")


def exibir_cursos_do_aluno(aluno, cursos):
    if not aluno:
        print("[!] Aluno não encontrado.")
        return
    print(f"\n--- Cursos de {aluno.nome} ---")
    if not cursos:
        print("  Nenhum curso.")
        return
    for c in cursos:
        print(f"  [{c.id}] {c.nome}")
    print()


def exibir_alunos_do_curso(curso, alunos):
    if not curso:
        print("[!] Curso não encontrado.")
        return
    print(f"\n--- Alunos em {curso.nome} ---")
    if not alunos:
        print("  Nenhum aluno.")
        return
    for a in alunos:
        print(f"  [{a.id}] {a.nome}")
    print()
