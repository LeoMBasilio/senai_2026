# Models/mago.py — subclasse de Personagem que representa um mago
# O mago causa mais dano por nivel (multiplicador 3) mas tem menos HP (80 vs 120 do guerreiro).

from Models.personagem import Personagem


class Mago(Personagem):
    __mapper_args__ = {"polymorphic_identity": "mago"}

    def atacar(self, alvo: Personagem) -> int:
        # Fórmula: poder_magico * nivel * 3 — multiplicador maior que o do guerreiro.
        # Isso reflete o conceito de "vidro de canhão": muito dano, pouca vida.
        dano = (self.poder_magico or 8) * self.nivel * 3
        alvo.hp = max(0, alvo.hp - dano)
        return dano
