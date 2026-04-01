if __name__ == "__main__":
    soma = 0
    for i in range(1, 11):
        numero = int(input(f"Digite o {i}º número: "))
        
        numero_par = numero % 2

        if numero_par == 0:
            soma += 1
        else:
            soma_impar += 1
    print(f"A soma dos números pares é: {soma}")
    print(f"A soma dos números imapares é: {soma_impar}")