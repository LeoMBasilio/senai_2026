from Models.models import LinhaTempo, Evento, Viagem, Viajante


def exibir_evento(e: Evento):
    tag = " [ALTERADO]" if e.alterado else ""
    print(f"    {e.ano}: {e.descricao}{tag}")
    if e.alterado and e.descricao_original:
        print(f"          (original: {e.descricao_original})")


def exibir_linha_tempo(lt: LinhaTempo, eventos: list[Evento]):
    tag = " *** ORIGINAL ***" if lt.original else ""
    print(f"\n  Linha do Tempo #{lt.id}: {lt.nome}{tag}")
    if lt.descricao:
        print(f"    {lt.descricao}")
    print("    Eventos:")
    if not eventos:
        print("      (sem eventos)")
    for e in eventos:
        exibir_evento(e)


def exibir_todas_linhas(linhas: list[LinhaTempo], eventos_por_linha: dict[int, list[Evento]]):
    print("\n" + "=" * 60)
    print("  LINHAS DO TEMPO")
    print("=" * 60)
    for lt in linhas:
        exibir_linha_tempo(lt, eventos_por_linha.get(lt.id, []))


def exibir_viagem(v: Viagem):
    print(f"  Viagem #{v.id} | Viajante: {v.viajante_id} | Ano: {v.ano_destino}")
    print(f"    Alteração: {v.alteracao}")


def exibir_historico(viajante: Viajante, viagens: list[Viagem]):
    print(f"\n=== Histórico de {viajante.nome} ===")
    if not viagens:
        print("  Nenhuma viagem realizada.")
    for v in viagens:
        exibir_viagem(v)
