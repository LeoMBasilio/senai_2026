if __name__ == "__main__":
    num = int(input("Digite um número inteiro: "))
    cont = 0

    while cont < 10:
        cont += 1
        resultado = num * (cont)
        print(f"{num} x {cont} = {resultado}")