# Controllers/usuario_controller.py — camada de lógica do ex1
# Responsabilidade: orquestrar as operações no banco sem expor detalhes de SQL à View.
# O Controller NUNCA imprime nada — só processa dados e os retorna para quem chamou.

from Models.usuario import Usuario


def inicializar():
    # Deve ser chamada uma vez no início do programa para garantir que a tabela existe.
    Usuario.criar_tabela()


def inserir_usuario(nome: str, email: str) -> Usuario:
    # Abre uma sessão (transação) para fazer o INSERT.
    s = Usuario.session()
    try:
        usuario = Usuario(nome=nome, email=email)  # cria o objeto em memória
        s.add(usuario)      # agenda o INSERT para quando o commit for chamado
        s.commit()          # executa o INSERT no banco de fato
        s.refresh(usuario)  # recarrega o objeto do banco para pegar o id gerado
        return usuario
    except Exception as e:
        # rollback() desfaz todas as operações da sessão em caso de erro,
        # evitando dados inconsistentes no banco.
        s.rollback()
        raise e  # repassa o erro para que o main.py possa tratá-lo
    finally:
        # finally garante que a sessão seja SEMPRE fechada, mesmo em caso de exceção.
        # Fechar libera a conexão de volta ao pool do SQLAlchemy.
        s.close()


def listar_usuarios() -> list[Usuario]:
    s = Usuario.session()
    try:
        # s.query(Usuario).all() gera SELECT * FROM usuarios e retorna
        # uma lista de objetos Usuario (um por linha da tabela).
        return s.query(Usuario).all()
    finally:
        s.close()
