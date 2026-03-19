if __name__ == "__main__":

    nome = input("Digite seu nome: ")
    sexo = input("Digite seu sexo (M/F): ")
    estado_civil = input("Digite seu estado civil: ")

    if sexo.upper() == "F": #caso o "f" seja minusculo uso o .lower()
        if estado_civil.lower() == "casada":
            anos_casada = int(input("Digite há quantos anos você é casada: "))
    else:
        print("Sexo masculino é considerado.")