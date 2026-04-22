# Views/pagamento_view.py — camada de apresentação do ex7
# Recebe o resultado já processado como string — não sabe se foi Cartão ou Pix.


def exibir_resultado(pagamento, resultado: str):
    # O número do pagamento é exibido para rastreabilidade.
    print(f"[#{pagamento.id}] {resultado}")
