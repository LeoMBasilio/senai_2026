from Models.personagem import Personagem


class Guerreiro(Personagem):
    __mapper_args__ = {"polymorphic_identity": "guerreiro"}

    def atacar(self, alvo: Personagem) -> int:
        dano = (self.forca or 10) * self.nivel * 2
        alvo.hp = max(0, alvo.hp - dano)
        return dano
