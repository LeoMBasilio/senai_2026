# Controllers/usuario_repository.py — camada de lógica do ex8
# Implementa o padrão Repository: encapsula todo o acesso ao banco em uma classe.
# A vantagem é que o código externo interage com UsuarioRepository sem saber nada
# de SQLAlchemy — basta chamar salvar(), listar(), etc.

from Models.usuario import Usuario


class UsuarioRepository:
    def __init__(self):
        # Garante que a tabela existe ao instanciar o repositório.
        Usuario.criar_tabela()

    def salvar(self, nome: str, email: str) -> Usuario:
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

    def listar(self) -> list[Usuario]:
        s = Usuario.session()
        try:
            return s.query(Usuario).all()
        finally:
            s.close()

    def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        s = Usuario.session()
        try:
            # .first() retorna None se não encontrar, evitando exceção desnecessária.
            return s.query(Usuario).filter_by(id=usuario_id).first()
        finally:
            s.close()

    def deletar(self, usuario_id: int) -> bool:
        s = Usuario.session()
        try:
            usuario = s.query(Usuario).filter_by(id=usuario_id).first()
            if not usuario:
                return False  # retorna False em vez de lançar exceção — convenção do padrão
            s.delete(usuario)
            s.commit()
            return True
        except Exception as e:
            s.rollback()
            raise e
        finally:
            s.close()
