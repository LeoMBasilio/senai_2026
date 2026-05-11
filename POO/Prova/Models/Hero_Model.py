from sqlalchemy import Column, Integer, String
from Models.Base_Model import Base


class Heroi(Base):
    __tablename__ = "herois"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    classe = Column(String, nullable=False)
    nivel = Column(Integer, default=1)
    pontos_experiencia = Column(Integer, default=0)

    def subi_nivel(self):
        while self.pontos_experiencia >= self.nivel * 100:
            self.pontos_experiencia -= self.nivel * 100
            self.nivel += 1

    def ganhar_experiencia(self, xp):
        self.pontos_experiencia += xp
        self.subi_nivel()

    def resumo(self):
        return f"[{self.id}] {self.nome} | {self.classe.capitalize()} | Nível {self.nivel} | XP {self.pontos_experiencia}/{self.nivel * 100}"
