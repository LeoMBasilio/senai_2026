"""Mini-RPG: batalha entre personagens com herança e polimorfismo."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

_db = os.path.join(os.path.dirname(__file__), "rpg.db")
if os.path.exists(_db):
    os.remove(_db)

from Controllers.personagem_controller import (
    inicializar, criar_guerreiro, criar_mago, criar_arqueiro,
    listar_personagens, batalha,
)
from Views.personagem_view import exibir_lista, exibir_batalha

inicializar()

thor = criar_guerreiro("Thor", nivel=3, hp=150, forca=14)
gandalf = criar_mago("Gandalf", nivel=3, hp=90, poder_magico=12)
legolas = criar_arqueiro("Legolas", nivel=3, hp=120, precisao=11)

exibir_lista(listar_personagens())

rodadas, vencedor, perdedor = batalha(thor, gandalf)
exibir_batalha(rodadas, vencedor, perdedor)

rodadas2, vencedor2, perdedor2 = batalha(vencedor, legolas)
exibir_batalha(rodadas2, vencedor2, perdedor2)
