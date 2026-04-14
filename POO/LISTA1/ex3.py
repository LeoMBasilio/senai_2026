class ContaJogador:
    def __init__(self, nome):
        self.nome = nome
        self.__xp = 0

    def ganhar_xp(self, xp):
        self.__xp += xp

        return f"Xp ganho {xp}"
    
    def gastar_xp(self, xp):
        self.__xp -= xp

        return f'Xp gasto {xp}'
    
    def status(self):
        return f'Nome: {self.nome}\nXp: {self.__xp}'
    
    def get_xp(self):
        return self.__xp
    
if __name__ == "__main__":
    conta1 = ContaJogador('Leo')

    print(conta1.status())
    print(conta1.ganhar_xp(1000))
    print(conta1.status())
    print(conta1.gastar_xp(10))
    print(conta1.status())