class MenuView:

    def executar(self, acoes):
        while True:
            print("\n[1] Registrar Herói  [2] Listar Heróis  [3] Criar Missão  [4] Concluir Missão  [0] Sair")
            opcao = input(">> ").strip()
            if opcao == "0":
                break
            elif opcao in acoes:
                acoes[opcao]()
            else:
                print("Opção inválida.")

    def exibir_herois(self, herois):
        if not herois:
            print("Nenhum herói cadastrado.")
            return
        for heroi in herois:
            print(f"\n{heroi.resumo()}")
            for missao in heroi.missoes:
                print(f"  - {missao.resumo()}")
