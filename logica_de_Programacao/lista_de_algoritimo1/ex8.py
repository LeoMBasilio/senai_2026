if __name__ == "__main__":
    vetor = []

    vetor.append(int(input("Digite o primeiro valor: ")))
    vetor.append(int(input("Digite o segundo valor: ")))
    vetor.append(int(input("Digite o terceiro valor: ")))

    vetor.sort(reverse=True)

    print("Vetor em ordem decrescente:", vetor)