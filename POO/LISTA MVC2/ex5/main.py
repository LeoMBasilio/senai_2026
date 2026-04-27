"""Sistema de avaliacao de filmes com notas, comentarios e ranking."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

_db = os.path.join(os.path.dirname(__file__), "filmes.db")
if os.path.exists(_db):
    os.remove(_db)

from Controllers.filme_controller import (
    inicializar, cadastrar_usuario, cadastrar_filme, avaliar,
    media_notas, listar_avaliacoes_filme, listar_filmes, ranking_filmes,
)
from Views.filme_view import exibir_catalogo, exibir_avaliacoes_filme, exibir_ranking

inicializar()

f1 = cadastrar_filme("Matrix", 1999, "Ficcao Cientifica", "Wachowski")
f2 = cadastrar_filme("O Poderoso Chefao", 1972, "Drama", "Francis Ford Coppola")
f3 = cadastrar_filme("Parasita", 2019, "Thriller", "Bong Joon-ho")
f4 = cadastrar_filme("Interestelar", 2014, "Ficcao Cientifica", "Christopher Nolan")

u1 = cadastrar_usuario("Pedro Alves", "pedro@email.com")
u2 = cadastrar_usuario("Fernanda Costa", "fernanda@email.com")
u3 = cadastrar_usuario("Ricardo Melo", "ricardo@email.com")

avaliar(u1.id, f1.id, 9.5, "Revolucionario para a epoca!")
avaliar(u2.id, f1.id, 8.0, "Classico, mas o CGI envelheceu.")
avaliar(u3.id, f1.id, 9.0)

avaliar(u1.id, f2.id, 10.0, "Obra-prima absoluta.")
avaliar(u2.id, f2.id, 9.5, "Perfeito em todos os aspectos.")
avaliar(u3.id, f2.id, 9.8)

avaliar(u1.id, f3.id, 9.2, "Final chocante!")
avaliar(u2.id, f3.id, 9.0)

avaliar(u3.id, f4.id, 8.5, "Trilha sonora incrivel.")
avaliar(u1.id, f4.id, 7.5, "Bonito, mas complexo demais.")

exibir_catalogo(listar_filmes())

for f in [f1, f2, f3, f4]:
    media = media_notas(f.id)
    avaliacoes = listar_avaliacoes_filme(f.id)
    exibir_avaliacoes_filme(f, avaliacoes, media)

exibir_ranking(ranking_filmes())
