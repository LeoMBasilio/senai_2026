'''Exercício 9 – Autenticação
Usuario com email e senha_hash. Cadastro e login.'''

from Controllers.auth_controller import inicializar, cadastrar, login
from Views.auth_view import exibir_cadastro, exibir_login, exibir_erro

inicializar()

# Cadastra dois usuários com senhas diferentes.
try:
    u1 = cadastrar("alice@email.com", "senha123")
    exibir_cadastro(u1)
    u2 = cadastrar("bruno@email.com", "bruno456")
    exibir_cadastro(u2)
except ValueError as e:
    exibir_erro(str(e))

print("\n[Tentativas de login]")

# Credenciais corretas — deve passar.
resultado = login("alice@email.com", "senha123")
exibir_login(resultado, "alice@email.com")

# Senha errada — deve falhar.
resultado = login("alice@email.com", "senhaerrada")
exibir_login(resultado, "alice@email.com")

# Email inexistente — deve falhar com a mesma mensagem genérica.
resultado = login("naoexiste@email.com", "qualquer")
exibir_login(resultado, "naoexiste@email.com")

# Tenta cadastrar email duplicado — deve lançar ValueError.
print("\n[Email duplicado]")
try:
    cadastrar("alice@email.com", "outrasenha")
except ValueError as e:
    exibir_erro(str(e))
