"""Sistema de Biblioteca: emprestimo e devolucao de livros."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

_db = os.path.join(os.path.dirname(__file__), "biblioteca.db")
if os.path.exists(_db):
    os.remove(_db)

from Controllers.biblioteca_controller import (
    inicializar, cadastrar_usuario, cadastrar_livro,
    pegar_emprestado, devolver,
    listar_livros_disponiveis, listar_emprestimos_ativos, historico_usuario,
)
from Views.biblioteca_view import (
    exibir_livros_disponiveis, exibir_emprestimos, exibir_devolucao,
)

inicializar()

ana = cadastrar_usuario("Ana Souza", "ana@email.com")
carlos = cadastrar_usuario("Carlos Lima", "carlos@email.com")

l1 = cadastrar_livro("Dom Casmurro", "Machado de Assis")
l2 = cadastrar_livro("O Alquimista", "Paulo Coelho")
l3 = cadastrar_livro("1984", "George Orwell")

exibir_livros_disponiveis(listar_livros_disponiveis())

emp1 = pegar_emprestado(ana.id, l1.id)
emp2 = pegar_emprestado(carlos.id, l2.id)
print(f"\n  Ana pegou '{l1.titulo}' emprestado.")
print(f"  Carlos pegou '{l2.titulo}' emprestado.")

exibir_livros_disponiveis(listar_livros_disponiveis())
exibir_emprestimos(listar_emprestimos_ativos(), "Emprestimos Ativos")

try:
    pegar_emprestado(carlos.id, l1.id)
except ValueError as e:
    print(f"\n  [REGRA] {e}")

devolver(emp1.id)
exibir_devolucao(emp1)

exibir_livros_disponiveis(listar_livros_disponiveis())
exibir_emprestimos(historico_usuario(ana.id), f"Historico de {ana.nome}")
