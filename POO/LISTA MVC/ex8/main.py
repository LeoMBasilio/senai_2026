'''Exercício 8 – Repositório
Criar UsuarioRepository com salvar, listar, buscar_por_id, deletar.'''

# main.py usa apenas a interface do repositório — não sabe nada de SQLAlchemy.
# Isso ilustra a vantagem do padrão: trocar o banco por um arquivo JSON, por exemplo,
# exigiria mudar só o UsuarioRepository, não o main nem a View.

from Controllers.usuario_repository import UsuarioRepository
from Views.usuario_view import exibir_salvo, exibir_lista, exibir_busca, exibir_deletado

repo = UsuarioRepository()

u1 = repo.salvar("Ana Souza", "ana@email.com")
u2 = repo.salvar("Bruno Lima", "bruno@email.com")
u3 = repo.salvar("Carla Dias", "carla@email.com")
for u in [u1, u2, u3]:
    exibir_salvo(u)

exibir_lista(repo.listar())

# Busca um usuário existente e um que não existe para testar os dois caminhos.
encontrado = repo.buscar_por_id(u2.id)
exibir_busca(encontrado, u2.id)

nao_encontrado = repo.buscar_por_id(999)
exibir_busca(nao_encontrado, 999)

# Deleta e lista novamente para confirmar a remoção.
ok = repo.deletar(u2.id)
exibir_deletado(ok, u2.id)

exibir_lista(repo.listar())
