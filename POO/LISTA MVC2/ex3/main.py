"""Sistema de Gerenciamento de Tarefas por categorias e status."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

_db = os.path.join(os.path.dirname(__file__), "tarefas.db")
if os.path.exists(_db):
    os.remove(_db)

from Controllers.tarefa_controller import (
    inicializar, criar_usuario, criar_categoria, criar_tarefa,
    atualizar_status, listar_por_categoria, listar_por_status,
    listar_tarefas_usuario, listar_categorias,
)
from Models.status_tarefa import StatusTarefa
from Views.tarefa_view import exibir_lista_tarefas, exibir_categorias

inicializar()

# Cria dois usuários para demonstrar que as tarefas ficam separadas por responsável.
joao = criar_usuario("Joao Silva")
maria = criar_usuario("Maria Oliveira")

# Cria três categorias — cada tarefa será obrigatoriamente vinculada a uma delas.
trabalho = criar_categoria("Trabalho", "Tarefas profissionais")
pessoal = criar_categoria("Pessoal", "Tarefas pessoais")
estudo = criar_categoria("Estudo", "Atividades de aprendizado")

exibir_categorias(listar_categorias())

# Cria cinco tarefas distribuídas entre os dois usuários e as três categorias.
t1 = criar_tarefa("Enviar relatorio mensal", "Relatorio de vendas de abril", joao.id, trabalho.id)
t2 = criar_tarefa("Comprar mantimentos", "Feira do mes", joao.id, pessoal.id)
t3 = criar_tarefa("Estudar SQLAlchemy", "Completar os exercicios de MVC", maria.id, estudo.id)
t4 = criar_tarefa("Reuniao de equipe", "Pauta: sprint planning", maria.id, trabalho.id)
t5 = criar_tarefa("Ler livro de Python", "Capitulos 5 a 8", joao.id, estudo.id)

# Exibe as tarefas de cada usuário — todas começam com status PENDENTE.
exibir_lista_tarefas(listar_tarefas_usuario(joao.id), f"Tarefas de {joao.nome}")
exibir_lista_tarefas(listar_tarefas_usuario(maria.id), f"Tarefas de {maria.nome}")

# Atualiza o status de três tarefas — demonstra a transição de estados.
atualizar_status(t1.id, StatusTarefa.EM_ANDAMENTO)
atualizar_status(t3.id, StatusTarefa.CONCLUIDA)
atualizar_status(t4.id, StatusTarefa.CONCLUIDA)

# Filtra por categoria e por status — demonstra as duas dimensões de consulta.
exibir_lista_tarefas(listar_por_categoria(trabalho.id), "Categoria: Trabalho")
exibir_lista_tarefas(listar_por_status(StatusTarefa.CONCLUIDA), "Tarefas Concluidas")
exibir_lista_tarefas(listar_por_status(StatusTarefa.PENDENTE), "Tarefas Pendentes")
