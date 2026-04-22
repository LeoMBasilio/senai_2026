'''Exercício 10 – Sistema de Tarefas
Usuario e Tarefa com CRUD completo.'''

# main.py orquestra todas as operações demonstrando cada letra do CRUD:
# Create (criar), Read (listar/buscar), Update (atualizar/concluir), Delete (deletar).

from Controllers.tarefas_controller import (
    inicializar,
    criar_usuario, listar_usuarios, buscar_usuario, atualizar_usuario, deletar_usuario,
    criar_tarefa, listar_tarefas_do_usuario, concluir_tarefa, atualizar_tarefa, deletar_tarefa,
)
from Views.tarefas_view import (
    exibir_usuario, exibir_lista_usuarios, exibir_tarefa, exibir_tarefas, exibir_deletado,
)

inicializar()

# CREATE — usuários
u1 = criar_usuario("Maria Oliveira", "maria@email.com")
u2 = criar_usuario("João Santos", "joao@email.com")
exibir_usuario(u1)
exibir_usuario(u2)

# READ — lista todos os usuários
exibir_lista_usuarios(listar_usuarios())

# UPDATE — atualiza nome do usuário
u1 = atualizar_usuario(u1.id, nome="Maria Clara Oliveira")
exibir_usuario(u1, acao="atualizado")

# CREATE — tarefas para cada usuário
t1 = criar_tarefa("Estudar SQLAlchemy", u1.id)
t2 = criar_tarefa("Fazer exercício de MVC", u1.id)
t3 = criar_tarefa("Revisar herança em Python", u1.id)
t4 = criar_tarefa("Entregar projeto", u2.id)
for t in [t1, t2, t3, t4]:
    exibir_tarefa(t)

# READ — lista tarefas de u1
exibir_tarefas(listar_tarefas_do_usuario(u1.id), u1.nome)

# UPDATE — conclui uma tarefa e atualiza o título de outra
t1 = concluir_tarefa(t1.id)
exibir_tarefa(t1, acao="concluída")

t2 = atualizar_tarefa(t2.id, "Finalizar exercício de MVC com testes")
exibir_tarefa(t2, acao="atualizada")

# DELETE — remove uma tarefa específica
ok = deletar_tarefa(t3.id)
exibir_deletado(ok, "Tarefa", t3.id)

# READ — confirma que t3 foi removida
exibir_tarefas(listar_tarefas_do_usuario(u1.id), u1.nome)

# DELETE — remove u2 (e sua tarefa t4 por cascade)
ok = deletar_usuario(u2.id)
exibir_deletado(ok, "Usuário", u2.id)

# READ — confirma que u2 foi removido
exibir_lista_usuarios(listar_usuarios())
