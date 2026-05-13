"""
pagination.py — Define como os resultados de listas são divididos em páginas.

Sem paginação, um endpoint como /api/produtos/ retornaria TODOS os produtos
de uma vez — problemático com milhares de registros (lento, pesado para o cliente).

Com paginação, a resposta inclui apenas uma "fatia" dos dados, mais links
para a próxima e anterior página.

Resposta paginada de exemplo:
{
    "count": 50,          ← total de itens no banco
    "total_pages": 5,     ← campo extra que adicionamos
    "next": "http://.../api/produtos/?page=2",
    "previous": null,
    "results": [...]      ← os itens desta página
}
"""

import math
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ProductPagination(PageNumberPagination):
    """
    Paginação customizada por número de página.
    O cliente navega com: ?page=2 ou ?page=3&page_size=5

    Herda de PageNumberPagination que já implementa toda a lógica base.
    Só precisamos personalizar os atributos e o formato da resposta.
    """

    # Quantidade de itens retornados por padrão quando o cliente não especifica
    page_size = 12

    # Nome do query param que permite ao cliente escolher quantos itens quer.
    # ?page_size=3 retorna 3 itens por página
    # Sem isso, o cliente não pode alterar o page_size.
    page_size_query_param = 'page_size'

    # Limite de segurança: mesmo que o cliente peça page_size=99999,
    # retornamos no máximo 100 itens. Protege o servidor de sobrecarga.
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Sobrescreve o método que monta o JSON de resposta paginada.
        Adicionamos o campo 'total_pages' que não existe na classe base.

        self.page.paginator.count = total de objetos no banco (para a query atual)
        self.get_page_size(request) = tamanho da página atual (respeitando max)
        math.ceil() arredonda para cima: 10 itens / 3 por página = ceil(3.33) = 4 páginas
        """
        total_pages = math.ceil(
            self.page.paginator.count / self.get_page_size(self.request)
        )

        return Response({
            'count': self.page.paginator.count,    # total de registros
            'total_pages': total_pages,            # campo extra calculado
            'next': self.get_next_link(),          # URL da próxima página (ou null)
            'previous': self.get_previous_link(),  # URL da página anterior (ou null)
            'results': data,                       # lista de itens desta página
        })
