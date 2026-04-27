from sqlalchemy import Column, Integer, String
from Models.base import Base


class Personagem(Base):
    __tablename__ = "personagens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    hp = Column(Integer, nullable=False, default=100)
    hp_max = Column(Integer, nullable=False, default=100)
    nivel = Column(Integer, nullable=False, default=1)
    tipo = Column(String(50), nullable=False)

    # colunas compartilhadas das subclasses (STI — Single Table Inheritance)
    forca = Column(Integer, nullable=True)
    poder_magico = Column(Integer, nullable=True)
    precisao = Column(Integer, nullable=True)

    __mapper_args__ = {
        "polymorphic_on": tipo,
        "polymorphic_identity": "personagem",
    }

    def atacar(self, alvo: "Personagem") -> int:
        raise NotImplementedError("Implemente atacar() na subclasse")

    def esta_vivo(self) -> bool:
        return self.hp > 0

    def resetar_hp(self):
        self.hp = self.hp_max

    def __repr__(self):
        return f"{self.tipo.capitalize()}(nome={self.nome!r}, hp={self.hp}/{self.hp_max}, nivel={self.nivel})"
