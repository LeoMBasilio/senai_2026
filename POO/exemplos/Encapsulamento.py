class Conta:
    def __init__(self, titular, saldo_inicial):
        self.titular   = titular           # público
        self.__saldo   = saldo_inicial     # privado
        self.__extrato = []               # privado

    def depositar(self, valor):
        if valor <= 0:
            print("Valor inválido para depósito.")
            return
        self.__saldo += valor
        self.__extrato.append(f"+ R${valor:.2f}")

    def sacar(self, valor):
        if valor > self.__saldo:
            print("Saldo insuficiente.")
            return
        self.__saldo -= valor
        self.__extrato.append(f"- R${valor:.2f}")

    def ver_saldo(self):         # getter
        return self.__saldo

    def ver_extrato(self):       # getter
        for linha in self.__extrato:
            print(linha)

# Uso correto — via métodos
c = Conta("Maria", 500)
c.depositar(200)
c.sacar(100)
print(c.ver_saldo())   # 600

# Acesso direto bloqueado:
# c.__saldo = 99999  →  não altera o saldo real!