class Carro:
    def __init__(self, modelo, cor):
        # self.atributo = valor  →  guarda dado neste objeto
        self.modelo = modelo
        self.cor    = cor
        self.ligado = False   # valor padrão

    def ligar(self):
        self.ligado = True
        print(f"{self.modelo} está ligado!")

    def descrever(self):
        estado = "ligado" if self.ligado else "desligado"
        print(f"{self.modelo}{self.cor} —{estado}")

# Instanciando dois objetos independentes
carro1 = Carro("Gol", "prata")
carro2 = Carro("Civic", "preto")

carro1.ligar()       # Gol está ligado!
carro2.descrever()   # Civic preto — desligado

carro1.modelo = 'fusca'