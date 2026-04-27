from Models.models import Filme, Avaliacao


def estrelas(nota: float) -> str:
    cheia = int(nota / 2)
    return "*" * cheia + "." * (5 - cheia)


def exibir_filme(f: Filme, media: float = None, total: int = 0):
    media_txt = f"{media:.1f} {estrelas(media)} ({total} avaliações)" if media else "sem avaliações"
    print(f"  [{f.id}] {f.titulo} ({f.ano}) | {f.genero or 'N/A'} | {media_txt}")


def exibir_catalogo(filmes: list[Filme]):
    print("\n=== Catálogo de Filmes ===")
    for f in filmes:
        exibir_filme(f)


def exibir_avaliacao(av: Avaliacao):
    print(f"    Usuário #{av.usuario_id}: {av.nota:.1f}/10 {estrelas(av.nota)}")
    if av.comentario:
        print(f"      \"{av.comentario}\"")


def exibir_avaliacoes_filme(f: Filme, avaliacoes: list[Avaliacao], media: float):
    print(f"\n=== Avaliações: {f.titulo} ===")
    print(f"  Média: {media if media else 'N/A'}")
    if not avaliacoes:
        print("  Ainda sem avaliações.")
    for av in avaliacoes:
        exibir_avaliacao(av)


def exibir_ranking(ranking: list[tuple]):
    print("\n=== Ranking de Filmes ===")
    print(f"  {'#':<3} {'Título':<35} {'Média':>6} {'Avaliações':>12}")
    print("  " + "-" * 60)
    for pos, (filme, media, total) in enumerate(ranking, 1):
        media_str = f"{media:.1f}" if media else "N/A"
        print(f"  {pos:<3} {filme.titulo:<35} {media_str:>6} {int(total or 0):>12}")
