class Inventario:
    def __init__(self):
        self.__nome = None
        self.__peso= None
        self.__preco= None
        self.__quant = None

    def set_preco(self, valor):
        if valor > 0 :
            self.__preco = valor
            return True
        return False
    
    def add_iten(self, nome, peso, quant, preco):
        if (peso < 0) or (quant < 0) or not self.set_preco(preco):
            return False
        self.__nome = nome
        self.__peso = peso
        self.__quant = quant
        return True
    
    def remove_iten(self):
        self.__nome = None
        self.__peso= None
        self.__preco= None
        self.__quant = None

    def Exbir_detalhes(self):
        return f"Nome: {self.__nome}\nPeso: {self.__peso}\nPreco: {self.__preco}\nQuantia: {self.__quant}"
    

if __name__ == "__main__":
    inv = Inventario()

    if inv.add_iten('lapis', 20, 70, 2.5):
        print('add')

    inv.remove_iten()

    print(inv.Exbir_detalhes())
