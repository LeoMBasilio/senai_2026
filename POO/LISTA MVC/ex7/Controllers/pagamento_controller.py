# Controllers/pagamento_controller.py — camada de lógica do ex7
# Cada função cria a subclasse correta e chama processar_pagamento() via polimorfismo.
# O Controller não precisa saber qual subclasse vai processar — só chama o método.

from Models.pagamento import Cartao, Pix, criar_tabelas, get_session


def inicializar():
    criar_tabelas()


def pagar_cartao(valor: float, numero_cartao: str, bandeira: str) -> tuple[Cartao, str]:
    s = get_session()
    try:
        pagamento = Cartao(valor=valor, numero_cartao=numero_cartao, bandeira=bandeira)
        s.add(pagamento)
        s.commit()
        s.refresh(pagamento)
        # processar_pagamento() aqui chama o método de Cartao (polimorfismo em ação).
        resultado = pagamento.processar_pagamento()
        return pagamento, resultado
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def pagar_pix(valor: float, chave_pix: str) -> tuple[Pix, str]:
    s = get_session()
    try:
        pagamento = Pix(valor=valor, chave_pix=chave_pix)
        s.add(pagamento)
        s.commit()
        s.refresh(pagamento)
        # processar_pagamento() aqui chama o método de Pix.
        resultado = pagamento.processar_pagamento()
        return pagamento, resultado
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()
