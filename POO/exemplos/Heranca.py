class Funcionario:
    def __init__(self, nome, salario):
        self.nome    = nome
        self.salario = salario

    def apresentar(self):
        print(f"Funcionário:{self.nome} | Salário: R${self.salario:.2f}")

    def calcular_bonus(self):
        return self.salario * 0.05   # bônus padrão: 5%


class Gerente(Funcionario):       # herda de Funcionario
    def __init__(self, nome, salario, equipe):
        super().__init__(nome, salario)  # chama __init__ do pai
        self.equipe = equipe

    def calcular_bonus(self):         # sobrescreve o método
        return self.salario * 0.20   # gerente ganha 20%

    def apresentar(self):
        super().apresentar()            # reutiliza o pai
        print(f"  Gerente de{self.equipe}")


class Estagiario(Funcionario):
    def __init__(self, nome, salario, curso):
        super().__init__(nome, salario)
        self.curso = curso

    def calcular_bonus(self):
        return 0                        # estagiário sem bônus

# Usando as classes
f = Funcionario("Ana",    3000)
g = Gerente("Carlos", 8000, "TI")
e = Estagiario("Pedro", 1200, "Ciência da Computação")

g.apresentar()
print(g.calcular_bonus())  # 1600.0