class Arena:
    def __init__(self, L, A):
        self.largura = L
        self.altura = A

    def calcular_area(self):
        area = self.largura * self.altura

        return area
    
    def calcular_perimetro(self):
        perimetro = (2 *self.largura) + (2*self.altura)

        return perimetro
    
if __name__ == "__main__":
    arena = Arena(2,5)

    print(arena.calcular_area())
    print(arena.calcular_perimetro())