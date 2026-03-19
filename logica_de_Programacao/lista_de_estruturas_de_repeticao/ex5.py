if __name__ == "__main__":
    numeros = [] # Lista para armazenar os números digitados
    cont = 0 # Contador para controlar o número de entradas
    soma = 0 # Variável para armazenar a soma dos números, iniciada em 0

    while cont < 10: # Loop para solicitar 10 números ao usuário
        cont += 1 # Incrementa o contador a cada iteração
        numeros.append(int(input("Digite um número: "))) # Solicita um número ao usuário, converte para inteiro e adiciona à lista

    for num in numeros: # num recebe cada número da lista numeros
        soma += num # Soma o número atual (num) à variável soma
    print("A soma dos números é: ", soma) # Exibe a soma total dos números digitados pelo usuário