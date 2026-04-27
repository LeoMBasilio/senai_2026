from Models.models import Vilao, Capanga, Crime, DominioCriminal


STATUS_ICONE = {
    "planejado": "[PLAN]",
    "em_execucao": "[EXEC]",
    "concluido": "[DONE]",
    "falhou": "[FAIL]",
}


def exibir_vilao(v: Vilao):
    codinome = f' aka "{v.codinome}"' if v.codinome else ""
    print(f"  [{v.id}] {v.nome}{codinome} | Poder Mundial: {v.poder_mundial}")


def exibir_capanga(c: Capanga):
    print(f"    - {c.nome} ({c.habilidade}) | Lealdade: {c.lealdade}%")


def exibir_crime(cr: Crime):
    icone = STATUS_ICONE.get(cr.status.value, "?")
    print(f"    {icone} [{cr.id}] {cr.nome} | Recompensa: +{cr.recompensa_poder} poder | {cr.status.value}")
    if cr.descricao:
        print(f"         {cr.descricao}")


def exibir_ficha_vilao(v: Vilao, capangas: list[Capanga], crimes: list[Crime]):
    print(f"\n{'='*55}")
    exibir_vilao(v)
    print(f"  Capangas ({len(capangas)}):")
    if not capangas:
        print("    Nenhum capanga.")
    for c in capangas:
        exibir_capanga(c)
    print(f"  Crimes ({len(crimes)}):")
    if not crimes:
        print("    Nenhum crime registrado.")
    for cr in crimes:
        exibir_crime(cr)


def exibir_resultado_crime(crime: Crime, sucesso: bool):
    if sucesso:
        print(f"\n  SUCESSO! '{crime.nome}' concluído. +{crime.recompensa_poder} de poder mundial!")
    else:
        print(f"\n  FALHA! '{crime.nome}' foi frustrado. Poder reduzido.")


def exibir_ranking(viloes: list[Vilao]):
    print("\n" + "=" * 55)
    print("  RANKING DE DOMÍNIO MUNDIAL")
    print("=" * 55)
    for pos, v in enumerate(viloes, 1):
        codinome = f' ({v.codinome})' if v.codinome else ""
        barra = "#" * (v.poder_mundial // 5) if v.poder_mundial > 0 else "-"
        print(f"  {pos}. {v.nome}{codinome:<20} | {v.poder_mundial:>4} pts {barra}")
    print("=" * 55)
