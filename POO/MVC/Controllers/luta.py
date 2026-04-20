def lutar(p1, p2):
    while p1.hp > 0 and p2.hp > 0:
        p1.atacar(p2)
        if p2.hp > 0:
            p2.atacar(p1)

    if p1.hp > 0:
        return f"{p1.nome} venceu!"
    else:
        return f"{p2.nome} venceu!"
