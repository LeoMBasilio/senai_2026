import random
from Models.personagem import Personagem


class Arqueiro(Personagem):
    __mapper_args__ = {"polymorphic_identity": "arqueiro"}

    def atacar(self, alvo: Personagem):
        critico = random.random() < 0.25
        dano = int((self.precisao or 9) * self.nivel * 2.5 * (2 if critico else 1))
        alvo.hp = max(0, alvo.hp - dano)
        return dano, critico
