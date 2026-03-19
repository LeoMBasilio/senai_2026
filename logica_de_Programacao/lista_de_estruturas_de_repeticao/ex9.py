if __name__ == "__main__":
    nome_aux = ""
    idade_aux = 0

    for i in range(1, 11):
        nome = input(f"Digite o nome da {i}ª pessoa: ")
        idade = int(input(f"Digite a idade da {i}ª pessoa: "))

        if nome_aux == "":
            nome_aux = nome
            idade_aux = idade
        else:
            if idade < idade_aux:
                nome_aux = nome
                idade_aux = idade
    print(f"A pessoa mais nova é {nome_aux} com {idade_aux} anos.")