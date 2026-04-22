# Views/auth_view.py — camada de apresentação do ex9
# Exibe resultados de autenticação sem revelar detalhes internos (como senha_hash).


def exibir_cadastro(usuario):
    print(f"[+] Cadastrado: id={usuario.id} | {usuario.email}")


def exibir_login(usuario, email: str):
    if usuario:
        print(f"[OK] Login bem-sucedido: id={usuario.id} | {usuario.email}")
    else:
        # Mensagem genérica — não revela se o email não existe ou a senha estava errada.
        # Isso evita que um atacante use a mensagem para descobrir quais emails estão cadastrados.
        print(f"[FALHA] Login inválido para '{email}'")


def exibir_erro(mensagem: str):
    print(f"[ERRO] {mensagem}")
