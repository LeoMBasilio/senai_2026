'''Exercício 7 – Herança
Pagamento base com subclasses Cartao e Pix. Método processar_pagamento.'''

# main.py não precisa saber detalhes de Cartao ou Pix — só chama o controller
# correto e exibe o resultado. Isso demonstra o benefício do polimorfismo.

from Controllers.pagamento_controller import inicializar, pagar_cartao, pagar_pix
from Views.pagamento_view import exibir_resultado

inicializar()

# Dois pagamentos via cartão com bandeiras diferentes.
p1, r1 = pagar_cartao(250.00, "4111111111111234", "Visa")
exibir_resultado(p1, r1)

p2, r2 = pagar_cartao(89.90, "5500000000005678", "Mastercard")
exibir_resultado(p2, r2)

# Dois pagamentos via Pix com chaves diferentes (email e telefone).
p3, r3 = pagar_pix(150.00, "joao@email.com")
exibir_resultado(p3, r3)

p4, r4 = pagar_pix(320.50, "11999998888")
exibir_resultado(p4, r4)
