# Models/guerreiro.py — subclasse de Personagem que representa um guerreiro
# Herda toda a estrutura da tabela de Personagem (STI) e define apenas o comportamento de ataque.

from Models.personagem import Personagem


class Guerreiro(Personagem):
    # polymorphic_identity: valor que será gravado na coluna "tipo" quando um Guerreiro for salvo.
    # O SQLAlchemy usa este valor para reconstruir objetos Guerreiro ao ler do banco.
    __mapper_args__ = {"polymorphic_identity": "guerreiro"}

    def atacar(self, alvo: Personagem) -> int:
        # Fórmula: forca * nivel * 2
        # "or 10" é um fallback caso forca seja None (registro antigo sem valor).
        # max(0, ...) evita que o hp do alvo fique negativo — hp mínimo é 0 (morto).
        dano = (self.forca or 10) * self.nivel * 2
        alvo.hp = max(0, alvo.hp - dano)
        return dano  # retorna o dano causado para o Controller registrar no log de batalha
