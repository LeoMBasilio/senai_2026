"""Sistema de Viloes: capangas, crimes e disputa pelo dominio mundial."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

_db = os.path.join(os.path.dirname(__file__), "viloes.db")
if os.path.exists(_db):
    os.remove(_db)

from Controllers.vilao_controller import (
    inicializar, criar_vilao, contratar_capanga, planejar_crime,
    executar_crime, conquistar_territorio, ranking_viloes,
    buscar_vilao, listar_capangas, listar_crimes,
)
from Views.vilao_view import exibir_ficha_vilao, exibir_resultado_crime, exibir_ranking

inicializar()

joker = criar_vilao("Arthur Fleck", "Joker")
thanos = criar_vilao("Thanos", "O Tita Louco")
magneto = criar_vilao("Max Eisenhardt", "Magneto")

contratar_capanga(joker.id, "Arlequina", "Acrobacia e Caos")
contratar_capanga(joker.id, "Pinguim", "Estrategia e Corrupcao")
contratar_capanga(thanos.id, "Gamora", "Combate e Assassinato")
contratar_capanga(thanos.id, "Ebony Maw", "Telecinese e Tortura")
contratar_capanga(thanos.id, "Corvus Glaive", "Estrategia Militar")
contratar_capanga(magneto.id, "Pyro", "Controle do Fogo")

c1 = planejar_crime(joker.id, "Assalto ao Banco de Gotham", "Roubar as reservas de ouro", 15)
c2 = planejar_crime(joker.id, "Envenenar o suprimento de agua", "Caos na cidade", 25)
c3 = planejar_crime(thanos.id, "Reunir as Joias do Infinito", "Coletar todas as 6 joias", 50)
c4 = planejar_crime(thanos.id, "Estalar os dedos", "Eliminar 50% do universo", 100)
c5 = planejar_crime(magneto.id, "Inverter os polos magneticos", "Destruir a grade eletrica global", 40)

for crime_id in [c1.id, c2.id, c3.id, c4.id, c5.id]:
    crime, sucesso = executar_crime(crime_id)
    exibir_resultado_crime(crime, sucesso)

conquistar_territorio(thanos.id, "O Universo Inteiro")
conquistar_territorio(magneto.id, "Ilha Genosha")

for v_id in [joker.id, thanos.id, magneto.id]:
    v = buscar_vilao(v_id)
    exibir_ficha_vilao(v, listar_capangas(v_id), listar_crimes(v_id))

exibir_ranking(ranking_viloes())
