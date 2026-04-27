"""Sistema de Biblioteca: emprestimo e devolucao de livros."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

# Remove o banco antes de cada execução para evitar conflitos de email único e dados duplicados.
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

# Cadastra leitores e livros — nenhuma dependência entre eles neste ponto.
ana = cadastrar_usuario("Ana Souza", "ana@email.com")
carlos = cadastrar_usuario("Carlos Lima", "carlos@email.com")

l1 = cadastrar_livro("Dom Casmurro", "Machado de Assis")
l2 = cadastrar_livro("O Alquimista", "Paulo Coelho")
l3 = cadastrar_livro("1984", "George Orwell")

# Exibe o acervo completo: todos os livros estão disponíveis inicialmente.
exibir_livros_disponiveis(listar_livros_disponiveis())

# Ana pega l1 e Carlos pega l2 — ambos ficam indisponíveis.
emp1 = pegar_emprestado(ana.id, l1.id)
emp2 = pegar_emprestado(carlos.id, l2.id)
print(f"\n  Ana pegou '{l1.titulo}' emprestado.")
print(f"  Carlos pegou '{l2.titulo}' emprestado.")

# Agora só l3 deve aparecer como disponível.
exibir_livros_disponiveis(listar_livros_disponiveis())
exibir_emprestimos(listar_emprestimos_ativos(), "Emprestimos Ativos")

# Testa a regra de negócio: tenta pegar l1 que já está com Ana — deve lançar ValueError.
try:
    pegar_emprestado(carlos.id, l1.id)
except ValueError as e:
    print(f"\n  [REGRA] {e}")

# Ana devolve l1 — o livro volta a disponível.
devolver(emp1.id)
exibir_devolucao(emp1)

# l1 e l3 devem aparecer disponíveis agora.
exibir_livros_disponiveis(listar_livros_disponiveis())

# Histórico da Ana: mostra o empréstimo já encerrado com data de devolução preenchida.
exibir_emprestimos(historico_usuario(ana.id), f"Historico de {ana.nome}")
