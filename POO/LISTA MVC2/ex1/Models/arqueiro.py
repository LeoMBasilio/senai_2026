# Models/arqueiro.py — subclasse de Personagem que representa um arqueiro
# Diferencial: pode causar DANO CRÍTICO (25% de chance) que dobra o dano.
# Único tipo que retorna uma tupla (dano, critico) em vez de apenas um inteiro.

import random
from Models.personagem import Personagem


class Arqueiro(Personagem):
    __mapper_args__ = {"polymorphic_identity": "arqueiro"}

    def atacar(self, alvo: Personagem):
        # random.random() gera um float entre 0.0 e 1.0.
        # Se o valor for menor que 0.25, é um golpe crítico (probabilidade de 25%).
        critico = random.random() < 0.25

        # int(...) converte o resultado float para inteiro (dano não tem fração).
        # (2 if critico else 1) dobra o dano em caso de crítico.
        dano = int((self.precisao or 9) * self.nivel * 2.5 * (2 if critico else 1))
        alvo.hp = max(0, alvo.hp - dano)

        # Retorna uma tupla para que o Controller saiba se houve crítico e exiba no log.
        # Os outros personagens retornam apenas int — o Controller trata os dois casos.
        return dano, critico
