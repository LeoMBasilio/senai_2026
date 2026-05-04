from Models.Hero_Model import Heroi
from Models.Missao_Model import Missao
from Models.Database_Model import Session


class GuildaController:

    def __init__(self):
        self.db = Session()

    def registrar_heroi(self, nome, classe):
        heroi = Heroi(nome=nome, classe=classe, nivel=1, pontos_experiencia=0)
        self.db.add(heroi)
        self.db.commit()
        return heroi

    def listar_herois(self):
        return self.db.query(Heroi).all()

    def buscar_heroi(self, id):
        return self.db.query(Heroi).filter(Heroi.id == id).first()

    def remover_heroi(self, id):
        heroi = self.buscar_heroi(id)
        if not heroi:
            return False
        self.db.query(Missao).filter(Missao.heroi_id == id).delete()
        self.db.delete(heroi)
        self.db.commit()
        return True

    def criar_missao(self, titulo, descricao, recompensa_xp, heroi_id):
        if not self.buscar_heroi(heroi_id):
            print(f"Herói {heroi_id} não encontrado.")
            return None
        missao = Missao(titulo=titulo, descricao=descricao, recompensa_xp=recompensa_xp, heroi_id=heroi_id)
        self.db.add(missao)
        self.db.commit()
        return missao

    def concluir_missao(self, missao_id):
        missao = self.db.query(Missao).filter(Missao.id == missao_id).first()
        if not missao:
            print(f"Missão {missao_id} não encontrada.")
            return False
        if missao.status == "concluida":
            print(f"Missão '{missao.titulo}' já concluída.")
            return False
        missao.concluir()
        missao.heroi.ganhar_experiencia(missao.recompensa_xp)
        self.db.commit()
        return True
