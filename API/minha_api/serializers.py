# ============================================================
# serializers.py — Converte dados entre Python e JSON
#
# Quando a API recebe ou envia dados, eles precisam estar em
# formato JSON (texto). O Serializer faz essa conversão:
#
#   Objeto Python  →  JSON   (para enviar na resposta)
#   JSON recebido  →  Python (para salvar no banco)
#
# Além disso, o Serializer valida os dados recebidos antes
# de qualquer coisa ser salva.
# ============================================================

from rest_framework import serializers  # ferramentas de serialização
from .models import Produto             # importa o model que vamos serializar


# ModelSerializer cria automaticamente o serializer baseado no Model.
# Não precisamos declarar cada campo manualmente — ele lê o Model.
class ProdutoSerializer(serializers.ModelSerializer):

    # A classe Meta configura o comportamento do serializer.
    class Meta:

        # Diz qual Model esse serializer representa.
        model = Produto

        # fields = '__all__' → inclui TODOS os campos do Model no JSON.
        # Alternativas:
        #   fields = ['id', 'nome', 'preco']  → inclui só esses campos
        #   exclude = ['criado_em']           → inclui tudo EXCETO criado_em
        fields = '__all__'

        # read_only_fields → campos que aparecem na RESPOSTA (GET)
        # mas são IGNORADOS se enviados na requisição (POST/PUT).
        # 'id' é gerado pelo banco automaticamente.
        # 'criado_em' é gerado pelo Django automaticamente.
        # Não faz sentido o usuário informar esses valores.
        read_only_fields = ['id', 'criado_em']
