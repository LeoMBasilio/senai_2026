if __name__ == "__main__":
    nome = input("Digite seu nome: ")
    num = int(input("Digite um número: "))

    cont = 0

    while cont < num:
        cont += 1
        print(cont, " - ", nome)