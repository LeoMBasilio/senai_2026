'''Crie um modelo Usuario com id, nome e email (único). Implemente criação da tabela, inserção de 3
usuários e listagem.'''

# main.py é o ponto de entrada da aplicação no padrão MVC.
# Ele NUNCA contém lógica de banco ou formatação — só coordena chamadas entre Controller e View.
# Isso mantém cada camada com uma única responsabilidade (princípio do SRP).

from Controllers.usuario_controller import inicializar, inserir_usuario, listar_usuarios
from Views.usuario_view import exibir_usuario_criado, exibir_lista

# Garante que a tabela 'usuarios' existe antes de qualquer operação.
inicializar()

# Lista de tuplas com os dados dos usuários a inserir.
# Manter os dados separados da lógica facilita adicionar ou remover usuários de teste.
usuarios_novos = [
    ("Alice Silva", "alice@email.com"),
    ("Bruno Costa", "bruno@email.com"),
    ("Carla Mendes", "carla@email.com"),
]

# Para cada par (nome, email), chama o Controller para inserir e a View para exibir.
# O main orquestra a sequência, mas não sabe como o insert funciona nem como formatar a saída.
for nome, email in usuarios_novos:
    u = inserir_usuario(nome, email)
    exibir_usuario_criado(u)

# Após inserir todos, solicita a listagem completa ao Controller e passa para a View exibir.
exibir_lista(listar_usuarios())
