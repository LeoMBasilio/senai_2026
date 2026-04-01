if __name__ == "__main__":
    soma = 0
    somab= 0
    somac= 0
    for i in range(1, 11):
        num = int(input(f"Digite o {i}º número: "))

        if num >= 0 and num <= 100:
            print(f"O número {num} está entre 0 e 100.")
            soma += 1
        elif num >= 101 and num <= 200:
            print(f"O número {num} está entre 101 e 200.")
            somab += 1
        else:
            print(f"O número {num} e maior que 200.")
            somac += 1

    print(f"A quantidade de números entre 0 e 100 é: {soma}")
    print(f"A quantidade de números entre 101 e 200 é: {somab}")   
    print(f"A quantidade de números maiores que 200 é: {somac}")