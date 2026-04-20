from Models.Mago import Mago
from Controllers.luta import lutar

def view():
    nome = input("Nome:")
    p1 = Mago(nome)

    nome = input('nome:')
    p2 = Mago(nome)

    print(lutar(p1, p2))
    