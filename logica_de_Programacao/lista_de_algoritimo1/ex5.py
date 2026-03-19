if __name__ == "__main__":
    valor1 = int(input("Digite o primeiro valor: "))

    if valor1 < 0:
        result = valor1 * 3
    else:
        result = valor1 * 2

    print(f"O resultado é: {result}")