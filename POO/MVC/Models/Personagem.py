class Personagem:
    def __init__(self, nome, hp, nivel):
        self.nome = nome
        self.hp = hp
        self.nivel = nivel

    def atacar(self, alvo):
        alvo.hp = alvo.hp - 5
        return alvo.hp