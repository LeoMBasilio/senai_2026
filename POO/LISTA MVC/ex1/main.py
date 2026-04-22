'''Crie um modelo Usuario com id, nome e email (único). Implemente criação da tabela, inserção de 3
usuários e listagem.'''

from Controllers.usuario_controller import inicializar, inserir_usuario, listar_usuarios
from Views.usuario_view import exibir_usuario_criado, exibir_lista

inicializar()

usuarios_novos = [
    ("Alice Silva", "alice@email.com"),
    ("Bruno Costa", "bruno@email.com"),
    ("Carla Mendes", "carla@email.com"),
]

for nome, email in usuarios_novos:
    u = inserir_usuario(nome, email)
    exibir_usuario_criado(u)

exibir_lista(listar_usuarios())
