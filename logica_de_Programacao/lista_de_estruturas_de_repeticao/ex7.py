if __name__ == "__main__":
    soma = 0
    
    for i in range(1, 11):
        idade = int(input(f"Digite a idade da pessoa {i}: "))
        soma += idade

    media = soma / 10
    print(f"A média de idade é: {media:.2f}")