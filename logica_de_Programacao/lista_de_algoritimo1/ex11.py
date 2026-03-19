if __name__ == "__main__":
    preco = float(input("Digite o preço do produto: "))
    condicao_pagamento = int(input("Digite a condição de pagamento (1-4): "))

    match condicao_pagamento:
      case 1:
        result = preco - (preco * 10 / 100)
      case 2:
        result = preco - (preco * 15 / 100)
      case 3:
        result = preco
      case 4:
        result = preco + (preco * 10 / 100)
      case _:
        print("Condição de pagamento inválida.")

    print(f"O preço final do produto é: R$ {result:.2f}")