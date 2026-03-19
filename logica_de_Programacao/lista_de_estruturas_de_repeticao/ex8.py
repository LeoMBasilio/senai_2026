if __name__ == "__main__":
    maior_idade = 0
    for i in range(1, 21):
        idade = int(input(f"Digite a idade da {i}ª pessoa: "))
        if idade >= 18:
            maior_idade += 1
    print(f"Total de pessoas maiores de idade: {maior_idade}")