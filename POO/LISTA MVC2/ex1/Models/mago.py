from Models.personagem import Personagem


class Mago(Personagem):
    __mapper_args__ = {"polymorphic_identity": "mago"}

    def atacar(self, alvo: Personagem) -> int:
        dano = (self.poder_magico or 8) * self.nivel * 3
        alvo.hp = max(0, alvo.hp - dano)
        return dano
