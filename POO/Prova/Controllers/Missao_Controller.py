from Models.Missao_Model import Missao
from Models.Hero_Model import Heroi
from Models.Database_Model import GetSession


class MissaoController:

    def __init__(self):
        self.Session = GetSession()

    def criar_missao(self, titulo: str, descricao: str, recompensa_xp: int, heroi_id: int) -> Missao | None:
        session = self.Session()
        heroi = session.query(Heroi).filter(Heroi.id == heroi_id).first()

        if not heroi:
            print(f"Herói com id {heroi_id} não encontrado.")
            session.close()
            return None

        missao = Missao(titulo=titulo, descricao=descricao, recompensa_xp=recompensa_xp, heroi_id=heroi_id)
        session.add(missao)
        session.commit()
        session.refresh(missao)
        session.close()
        return missao

    def concluir_missao(self, missao_id: int) -> bool:
        session = self.Session()
        missao = session.query(Missao).filter(Missao.id == missao_id).first()

        if not missao:
            print(f"Missão com id {missao_id} não encontrada.")
            session.close()
            return False

        if missao.status == "concluida":
            print(f"A missão '{missao.titulo}' já foi concluída anteriormente.")
            session.close()
            return False
        else:
            heroi = session.query(Heroi).filter(Heroi.id == missao.heroi_id).first()
            missao.concluir()
            heroi.ganhar_experiencia(missao.recompensa_xp)
            session.commit()
            session.close()
            return True
