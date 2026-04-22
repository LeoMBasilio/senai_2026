'''Exercício 3 – Busca e Filtro
Buscar produto por nome (LIKE) e listar produtos com preço maior que X.'''

# main.py conecta Controller e View sem conter lógica de banco ou formatação.

from Controllers.produto_controller import inicializar, inserir_produto, buscar_por_nome, listar_por_preco_maior_que
from Views.produto_view import exibir_produto_criado, exibir_busca, exibir_filtro_preco

inicializar()

# Popula o banco com produtos variados para ter dados suficientes para testar os filtros.
produtos_novos = [
    ("Notebook Dell", 3500.00, 10),
    ("Notebook Lenovo", 2800.00, 7),
    ("Mouse Gamer", 250.00, 40),
    ("Teclado Mecânico", 400.00, 20),
    ("Monitor 24\"", 1200.00, 15),
]

for nome, preco, estoque in produtos_novos:
    p = inserir_produto(nome, preco, estoque)
    exibir_produto_criado(p)

# Busca por "notebook" — deve retornar os dois notebooks independente de maiúsculas.
resultados = buscar_por_nome("notebook")
exibir_busca(resultados, "notebook")

# Filtra produtos acima de R$500 — deve retornar Notebook Dell, Notebook Lenovo e Monitor.
caros = listar_por_preco_maior_que(500.00)
exibir_filtro_preco(caros, 500.00)
