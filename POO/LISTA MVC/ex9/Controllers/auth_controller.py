# Controllers/auth_controller.py — camada de lógica do ex9
# Responsável por cadastro e autenticação. A senha nunca trafega em texto puro
# além do momento em que o usuário a digita — o hash é feito aqui antes de qualquer acesso.

import hashlib
from Models.usuario import Usuario


def inicializar():
    Usuario.criar_tabela()


def _hash_senha(senha: str) -> str:
    # SHA-256 é uma função de hash unidirecional: dado o hash, é computacionalmente
    # inviável descobrir a senha original. .encode() converte a string para bytes,
    # necessário para a função hashlib.
    # Em produção usaríamos bcrypt ou argon2 (com "salt"), mas SHA-256 ilustra o conceito.
    return hashlib.sha256(senha.encode()).hexdigest()


def cadastrar(email: str, senha: str) -> Usuario:
    s = Usuario.session()
    try:
        # Verifica duplicidade antes de inserir para dar uma mensagem de erro clara.
        existe = s.query(Usuario).filter_by(email=email).first()
        if existe:
            raise ValueError(f"Email '{email}' já cadastrado.")
        usuario = Usuario(email=email, senha_hash=_hash_senha(senha))
        s.add(usuario)
        s.commit()
        s.refresh(usuario)
        return usuario
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def login(email: str, senha: str) -> Usuario | None:
    s = Usuario.session()
    try:
        usuario = s.query(Usuario).filter_by(email=email).first()
        if not usuario:
            return None  # email não existe — retorna None em vez de revelar qual campo errou
        # Compara o hash da senha digitada com o hash armazenado.
        # Nunca descriptografamos a senha — só comparamos hashes.
        if usuario.senha_hash != _hash_senha(senha):
            return None
        return usuario
    finally:
        s.close()
