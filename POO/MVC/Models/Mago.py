from Models.Personagem import Personagem
#from Nome_pasta.arquivo import Class
class Mago(Personagem):
    def __init__(self,nome, hp=100, nivel=1):
        super().__init__(nome, hp, nivel)
        self.dano = 10

    def atacar(self, alvo):
        alvo.hp -= self.dano

        return alvo.hp