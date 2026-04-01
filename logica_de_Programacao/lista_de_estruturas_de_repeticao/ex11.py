if __name__ == "__main__":
    cont = 0

    while cont < 2:
        cont += 1

        num = int(input("Digite um número: "))

        if num > 8:
            print("Número maior que 8: ", num)
        else:
            print("Número menor ou igual a 8: ", num)
