if __name__ == "__main__":
    peso = float(input("Digite o peso da pessoa: "))
    altura = float(input("Digite a altura da pessoa: "))

    imc = peso / (altura ** 2) # ** e o operador de potenciação

    if imc < 18.5:
        print("A pessoa está abaixo do peso.")
    if imc >= 18.5 and imc < 25: 
    # and é o operador lógico de conjunção, 
    # ou seja, as duas condições precisam 
    # ser verdadeiras para o bloco de código ser executado
        print("A pessoa está com o peso normal.")
    if imc >= 25 and imc < 30:
        print("A pessoa está com sobrepeso.")
    if imc >= 30:
        print("A pessoa está com obesidade.")