if __name__ == "__main__":
    valorA = int(input("Digite o valor de A: "))
    valorB = int(input("Digite o valor de B: "))
    valorC = int(input("Digite o valor de C: "))

    soma = valorA + valorB
    
    if soma > valorC:
        print("A soma de A e B é maior que C.")
    else:
        print("A soma de A e B não é maior que C.")