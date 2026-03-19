if __name__ == "__main__":
    idades = [] # Lista para armazenar as idades digitadas
    cont = 0 # Contador para controlar o número de entradas
    soma = 0 # Variável para armazenar a soma das idades, iniciada em 0

    while cont < 10: # Loop para solicitar 10 idades ao usuário
        cont += 1 # Incrementa o contador a cada iteração
        idades.append(int(input("Digite a idade: "))) # Solicita uma idade ao usuário, converte para inteiro e adiciona à lista

    print('A soma das idades é: ', sum(idades)) # Exibe a soma total das idades digitadas pelo usuário usando a função sum() para calcular a soma da lista