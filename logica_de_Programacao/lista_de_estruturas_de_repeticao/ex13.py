if __name__ == "__main__":
    soma = 0
    for i in range(1, 11):
        num = int(input(f"Digite o {i}º número: "))

        if num >= 0 and num <= 100:
            print(f"O número {num} está entre 0 e 100.")
            soma += 1
    print(f"A quantidade de números entre 0 e 100 é: {soma}")