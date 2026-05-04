class ExibicaoView:

    def exibir_herois(self, herois: list):
        if not herois:
            print("\nNenhum herói cadastrado.")
            return

        print("\n========== HERÓIS DA GUILDA ==========")
        for heroi in herois:
            print(f"\n{heroi.resumo()}")
            self._exibir_missoes(heroi.missoes)
        print("======================================")

    def _exibir_missoes(self, missoes: list):
        pendentes = [m for m in missoes if m.status == "pendente"]
        concluidas = [m for m in missoes if m.status == "concluida"]

        if not pendentes and not concluidas:
            print("  Missões: nenhuma missão atribuída.")
            return

        if pendentes:
            print("  >> Missões Pendentes:")
            for missao in pendentes:
                print(f"     - {missao.resumo()}")

        if concluidas:
            print("  >> Missões Concluídas:")
            for missao in concluidas:
                print(f"     - {missao.resumo()}")
