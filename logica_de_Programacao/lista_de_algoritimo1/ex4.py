if __name__ == "__main__":
    valorA = float(input("Digite o valor de A: "))
    valorB = float(input("Digite o valor de B: "))

    if valorA != valorB:
        valorC = valorA * valorB
    if valorA == valorB:
        valorC = valorA + valorB

    print("O valor de C é: ", valorC)