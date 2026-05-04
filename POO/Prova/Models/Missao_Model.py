from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Models.Base_Model import Base


class Missao(Base):
    __tablename__ = "missoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    recompensa_xp = Column(Integer, nullable=False)
    status = Column(String, default="pendente")
    heroi_id = Column(Integer, ForeignKey("herois.id"), nullable=False)

    heroi = relationship("Heroi", backref="missoes")

    def concluir(self):
        self.status = "concluida"

    def resumo(self):
        return f"[{self.id}] {self.titulo} | {self.status.capitalize()} | {self.recompensa_xp} XP"
