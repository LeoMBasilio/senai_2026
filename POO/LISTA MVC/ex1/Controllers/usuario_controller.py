from Models.usuario import Usuario


def inicializar():
    Usuario.criar_tabela()


def inserir_usuario(nome: str, email: str) -> Usuario:
    s = Usuario.session()
    try:
        usuario = Usuario(nome=nome, email=email)
        s.add(usuario)
        s.commit()
        s.refresh(usuario)
        return usuario
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def listar_usuarios() -> list[Usuario]:
    s = Usuario.session()
    try:
        return s.query(Usuario).all()
    finally:
        s.close()
