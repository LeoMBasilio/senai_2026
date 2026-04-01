import random
import json
import os
import time

def Limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def Animacao_carregando(texto="Carregando", tempo=1.5):
    print(f"\n{texto}", end="", flush=True)
    for _ in range(3):
        time.sleep(tempo / 3)
        print(".", end="", flush=True)
    print("\n")

def Gerar_numro_aleatorio(n=100):
    return random.randint(1, n)

def Menu_reset():
    print("""
╔══════════════════════════════════╗
║        JOGAR NOVAMENTE?          ║
╠══════════════════════════════════╣
║          [ S ] SIM               ║
║          [ N ] NÃO               ║
╚══════════════════════════════════╝
""")
    escolha = input("Escolha: ")
    return escolha.lower() == 's'

def Gerar_pontuação(numero_aleatorio, palpite):
    diferenca = abs(numero_aleatorio - palpite)
    return max(0, 100 - diferenca * 10)

def Salvar_score(nome, score):
    arquivo = "logica_de_Programacao\scores.json"

    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            dados = json.load(f)
    else:
        dados = []

    dados.append({"nome": nome, "score": score})

    with open(arquivo, "w") as f:
        json.dump(dados, f, indent=4)

def Exibir_scores():
    arquivo = "logica_de_Programacao\scores.json"

    print("""
╔══════════════════════════════════════╗
║           🏆 SCOREBOARD 🏆           ║
╚══════════════════════════════════════╝
""")

    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            dados = json.load(f)

            ranking = sorted(dados, key=lambda x: x["score"], reverse=True)

            for i, entry in enumerate(ranking, 1):
                print(f"{i:>2}º │ {entry['nome']:<15} │ {entry['score']:>5} pts")

        print("\n╔══════════════════════════════════════╗")
        print("║        FIM DO RANKING               ║")
        print("╚══════════════════════════════════════╝\n")
    else:
        print("""
╔══════════════════════════════════════╗
║   Nenhum score registrado ainda.     ║
╚══════════════════════════════════════╝
""")

def Menu_dificuldade():
    print("""
╔══════════════════════════════════════╗
║         🎮 DIFICULDADE 🎮            ║
╠══════════════════════════════════════╣
║  1 │ Fácil      → 1 a 10   (10 tent.)║
║  2 │ Médio      → 1 a 50   (5 tent.) ║
║  3 │ Difícil    → 1 a 100  (2 tent.) ║
║  4 │ Hardcore   → 1 a 100  (1 tent.) ║
╚══════════════════════════════════════╝
""")
    escolha = input("Escolha uma opção: ").strip()

    match escolha:
        case "1":
            return 10, 10
        case "2":
            return 50, 5
        case "3":
            return 100, 2
        case "4":
            return 100, 1
        case _:
            print("Opção inválida.")
            time.sleep(1)
            return None, None

def Jogo_de_adivinhacao(numero_aleatorio, maximo_tentativas):
    tentativas = maximo_tentativas
    score_total = 0

    while tentativas > 0:
        Limpar_tela()

        print(f"""
╔══════════════════════════════════════╗
║ 🎯 TENTATIVAS RESTANTES: {tentativas:<2}          ║
║ ⭐ SCORE ATUAL: {score_total:<6}               ║
╚══════════════════════════════════════╝
""")

        try:
            palpite = int(input("Digite seu palpite: "))
        except ValueError:
            print("Entrada inválida!")
            time.sleep(1)
            continue

        pontos = Gerar_pontuação(numero_aleatorio, palpite)
        score_total += pontos

        print(f"+{pontos} pontos!")
        time.sleep(1)

        # bônus aleatório
        if palpite == Gerar_numro_aleatorio():
            bonus = random.randint(10, 50)
            print(f"🎉 BONUS! +{bonus} pontos")
            score_total += bonus
            time.sleep(1)

        if palpite < numero_aleatorio:
            print("🔻 Muito baixo!")
        elif palpite > numero_aleatorio:
            print("🔺 Muito alto!")
        else:
            time.sleep(1)
            return True, score_total

        time.sleep(1)
        tentativas -= 1

    return False, score_total

def main():
    reset = True

    while reset:
        Limpar_tela()

        print("""
╔══════════════════════════════════════╗
║        🎯 JOGO DE ADIVINHAÇÃO        ║
╠══════════════════════════════════════╣
║  1 │ Jogar                           ║
║  2 │ Ver Scoreboard                  ║
║  0 │ Sair                            ║
╚══════════════════════════════════════╝
""")

        escolha = input("Escolha uma opção: ").strip()

        Limpar_tela()
        Animacao_carregando("Processando")
        Limpar_tela()

        match escolha:

            case "1":
                max_num, maximo_tentativas = Menu_dificuldade()

                if max_num is not None:
                    Limpar_tela()
                    Animacao_carregando("Iniciando jogo")
                    Limpar_tela()

                    numero_aleatorio = Gerar_numro_aleatorio(max_num)

                    resultado, score = Jogo_de_adivinhacao(
                        numero_aleatorio, maximo_tentativas
                    )

                    Limpar_tela()

                    if resultado:
                        print(f"""
╔══════════════════════════════════════╗
║ 🏆 VOCÊ VENCEU!                      ║
║ 🎯 Número: {numero_aleatorio:<6}                    ║
╚══════════════════════════════════════╝
""")
                    else:
                        print(f"""
╔══════════════════════════════════════╗
║ 💀 VOCÊ PERDEU                      ║
║ 🎯 Número: {numero_aleatorio:<6}                   ║
╚══════════════════════════════════════╝
""")

                    nome = input(f"\n⭐ Score: {score}\nDigite seu nome: ")
                    Salvar_score(nome, score)

            case "2":
                Limpar_tela()
                Animacao_carregando("Carregando ranking")
                Limpar_tela()
                Exibir_scores()
                input("\nPressione ENTER para voltar...")

            case "0":
                print("""
╔══════════════════════════════════════╗
║        👋 ENCERRANDO JOGO           ║
╚══════════════════════════════════════╝
""")
                time.sleep(1)
                reset = False

            case _:
                print("Opção inválida!")
                time.sleep(1)

        if reset:
            time.sleep(1)
            Limpar_tela()
            reset = Menu_reset()


if __name__ == "__main__":
    main()