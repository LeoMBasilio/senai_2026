'''Exercício 6 – Many-to-Many
Aluno e Curso com relacionamento muitos-para-muitos.'''

from Controllers.escola_controller import (
    inicializar, inserir_aluno, inserir_curso, matricular,
    listar_cursos_do_aluno, listar_alunos_do_curso,
)
from Views.escola_view import (
    exibir_aluno_criado, exibir_curso_criado, exibir_matricula,
    exibir_cursos_do_aluno, exibir_alunos_do_curso,
)

inicializar()

# Cria alunos e cursos separadamente — a relação é criada depois via matricular().
a1 = inserir_aluno("Lucas Ferreira")
a2 = inserir_aluno("Mariana Torres")
a3 = inserir_aluno("Rafael Gomes")
for a in [a1, a2, a3]:
    exibir_aluno_criado(a)

c1 = inserir_curso("Python Avançado")
c2 = inserir_curso("Banco de Dados")
c3 = inserir_curso("Desenvolvimento Web")
for c in [c1, c2, c3]:
    exibir_curso_criado(c)

# Cada chamada a matricular() insere uma linha na tabela aluno_curso.
matricular(a1.id, c1.id); exibir_matricula(a1.id, c1.id)
matricular(a1.id, c2.id); exibir_matricula(a1.id, c2.id)
matricular(a2.id, c1.id); exibir_matricula(a2.id, c1.id)
matricular(a2.id, c3.id); exibir_matricula(a2.id, c3.id)
matricular(a3.id, c2.id); exibir_matricula(a3.id, c2.id)
matricular(a3.id, c3.id); exibir_matricula(a3.id, c3.id)

# Consulta pelos dois lados do relacionamento para demonstrar a bidirecionalidade.
aluno, cursos = listar_cursos_do_aluno(a1.id)
exibir_cursos_do_aluno(aluno, cursos)

curso, alunos = listar_alunos_do_curso(c1.id)
exibir_alunos_do_curso(curso, alunos)
