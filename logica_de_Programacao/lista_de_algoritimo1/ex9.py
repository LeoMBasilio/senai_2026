if __name__ == "__main__":
    altura = float(input("Digite a altura da pessoa: "))
    sexo = input("Digite o sexo da pessoa (M/F): ").upper()

    if sexo == "M":
        peso_ideal = (72.7 * altura) - 58
    elif sexo == "F":
        peso_ideal = (62.1 * altura) - 44.7

    print(f"O peso ideal para a pessoa é: {peso_ideal:.2f} kg")