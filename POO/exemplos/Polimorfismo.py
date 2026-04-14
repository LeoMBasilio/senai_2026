class Pagamento:
    def __init__(self, valor):
        self.valor = valor

    def processar(self):
        # método base — deve ser sobrescrito pelas filhas
        raise NotImplementedError("Implemente nas subclasses")

    def resumo(self):
        print(f"Valor: R${self.valor:.2f}")


class CartaoCredito(Pagamento):
    def __init__(self, valor, parcelas):
        super().__init__(valor)
        self.parcelas = parcelas

    def processar(self):     # comportamento do cartão
        parcela = self.valor / self.parcelas
        print(f"Cartão:{self.parcelas}x de R${parcela:.2f}")


class Pix(Pagamento):
    def processar(self):     # comportamento do Pix
        print(f"Pix: R${self.valor:.2f} — aprovado instantaneamente")


class Boleto(Pagamento):
    def processar(self):     # comportamento do boleto
        print(f"Boleto: R${self.valor:.2f} — vence em 3 dias úteis")


# Polimorfismo em ação — mesma chamada, resultados diferentes
pagamentos = [
    CartaoCredito(300.0, 3),
    Pix(150.0),
    Boleto(89.90),
]

for p in pagamentos:
    p.processar()   # cada objeto sabe o que fazer