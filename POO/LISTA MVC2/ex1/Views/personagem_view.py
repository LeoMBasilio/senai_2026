# Views/personagem_view.py — camada de apresentação do ex1 (mini-RPG)
# Responsabilidade: formatar e exibir o estado dos personagens e o log de batalha.
# Não contém lógica de jogo — só decide como as informações aparecem no terminal.

from Models.personagem import Personagem


def exibir_personagem(p: Personagem):
    # Exibe tipo em maiúsculo para destacar a classe do personagem.
    print(f"  [{p.tipo.upper()}] {p.nome} | HP: {p.hp}/{p.hp_max} | Nível: {p.nivel}")


def exibir_lista(personagens: list[Personagem]):
    print("\n=== Personagens ===")
    for p in personagens:
        exibir_personagem(p)


def exibir_rodada(rodada: dict):
    # Exibe "*** CRÍTICO! ***" apenas quando o arqueiro acertou um golpe crítico.
    critico_txt = " *** CRÍTICO! ***" if rodada["critico"] else ""

    # :<15 alinha o texto à esquerda em 15 caracteres — mantém as colunas alinhadas.
    # :>4 alinha o número à direita em 4 dígitos.
    print(
        f"  Rodada {rodada['rodada']:>2}: {rodada['atacante']:<15} ataca {rodada['defensor']:<15}"
        f" | Dano: {rodada['dano']:>4}{critico_txt}"
        f" | HP restante de {rodada['defensor']}: {rodada['hp_restante']}"
    )


def exibir_batalha(rodadas: list[dict], vencedor: Personagem, perdedor: Personagem):
    print(f"\n{'='*60}")
    # rodadas[0] contém os nomes dos combatentes da primeira rodada — servem como cabeçalho.
    print(f"  BATALHA: {rodadas[0]['atacante']} vs {rodadas[0]['defensor']}")
    print(f"{'='*60}")
    for r in rodadas:
        exibir_rodada(r)
    print(f"\n  VENCEDOR: {vencedor.nome} ({vencedor.tipo}) com {vencedor.hp} HP restante!")
    print(f"  {perdedor.nome} foi derrotado após {len(rodadas)} rodadas.")
    print(f"{'='*60}\n")
