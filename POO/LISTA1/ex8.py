class Personagem:
    def __init__(self, nome, poder):
        self.nome = nome
        self.poder = poder

    def __str__(self):
        return f'Nome: {self.nome}\nPoder: {self.poder}'

    def falar(self, poder):
        if poder > 8000:
            return f'{self.nome}: Mais de 8000!!'
        return f'{self.nome}: Verme insolente'
    
    def treino(self, tempo):
        self.poder *= tempo
    
if __name__ == "__main__":
    personagem1 = Personagem('goku', 500)
    personagem2 = Personagem('Napa', 1000)
    personagem3 = Personagem('vegeta', 5000)

    print(personagem3.falar(personagem1.poder))
    personagem1.treino(20)
    print(personagem2.falar(personagem1.poder))

