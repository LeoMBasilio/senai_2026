if __name__ == "__main__":
    soma = 0
    while True:
        num = int(input("Digite um número inteiro (ou -1 para sair): "))
        if num < 0:
            break
        soma += num

    print(f"A soma dos números digitados é: {soma}")