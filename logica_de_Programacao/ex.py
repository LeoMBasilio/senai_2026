
if __name__ == "__main__":
    flag = True
    while flag:
        while tentativas > 0:
            tentativas -= 1
            print(f"Você tem {tentativas} tentativas restantes.")

            choice = input("quer continuar: ")
            if choice.lower() == "sim":
                print("Continuando...")
            elif choice.lower() == "não":
                print("Encerrando o programa.")
                flag = False