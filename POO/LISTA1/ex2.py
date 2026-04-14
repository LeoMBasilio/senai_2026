class Nave:
    def __init__(self, nome, velocidade, vida):
        self.nome = nome
        self.velocidade = velocidade
        self.vida = vida
    
    def Exibir_Status(self):
        return f'Nome:{self.nome} | Velocidade: {self.velocidade} m/s | Vida: {self.vida}'
    
if __name__ == '__main__':
    nave = Nave('Falcon', '299 792 458', 1000 )

    print(nave.Exibir_Status())