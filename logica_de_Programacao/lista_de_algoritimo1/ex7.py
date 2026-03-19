if __name__ == "__main__":
    valor = int(input("Digite um valor: "))

    if valor % 2 == 0:
        soma = valor + 5
    else:
        soma = valor + 8

    print(f"O resultado é: {soma}")