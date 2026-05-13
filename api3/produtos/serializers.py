"""
serializers.py — Responsável por converter dados entre Python e JSON (e vice-versa).

O Serializer faz duas coisas:
  1. SERIALIZAÇÃO: converte objetos do banco (Model) em dicionários → JSON para o cliente
  2. DESSERIALIZAÇÃO: converte JSON recebido → valida os dados → salva no banco

Analogia: é como um tradutor entre o "idioma do banco de dados" e o "idioma do JSON".

ModelSerializer é um atalho que gera automaticamente os campos com base no Model,
evitando que você precise declarar campo por campo manualmente.
"""

from rest_framework import serializers
from .models import Categoria, Produto, Pedido, ItemPedido

# Importado aqui pois será usado pelo CustomTokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# =============================================================================
# CATEGORIA
# =============================================================================

class CategoriaSerializer(serializers.ModelSerializer):
    """
    Serializer simples para o model Categoria.
    Converte todos os campos do model para JSON.
    """

    class Meta:
        # Qual model este serializer representa
        model = Categoria

        # '__all__' inclui todos os campos do model automaticamente.
        # Equivale a fields = ['id', 'nome', 'descricao', 'ativa']
        # Cuidado: se o model tiver campo 'senha' ou dados sensíveis,
        # prefira listar os campos explicitamente.
        fields = '__all__'

        # read_only_fields = campos que aparecem na resposta (GET) mas são
        # IGNORADOS no recebimento (POST/PUT). O 'id' é gerado pelo banco,
        # então o cliente não deve — nem pode — enviá-lo.
        read_only_fields = ['id']


# =============================================================================
# PRODUTO
# =============================================================================

class ProdutoSerializer(serializers.ModelSerializer):
    """
    Serializer completo para Produto com campo extra calculado e validações.
    """

    # SerializerMethodField = campo calculado em Python, não existe no banco.
    # O DRF chama automaticamente o método get_<nome_do_campo>(self, obj).
    # Aqui usamos para mostrar o NOME da categoria em vez do ID numérico (FK).
    # Sem isso, a resposta mostraria "categoria": 1 — o cliente precisaria
    # fazer outra requisição para saber que "1" é "Bebidas".
    categoria_nome = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = '__all__'  # inclui também 'categoria_nome' por ser declarado acima
        read_only_fields = ['id', 'criado_em']
        # 'criado_em' é read_only pois auto_now_add=True no model —
        # o Django preenche automaticamente, o cliente não deve enviar.

    def get_categoria_nome(self, obj):
        """
        Método chamado pelo DRF para preencher o campo 'categoria_nome'.
        'obj' é a instância do Produto sendo serializada.
        Retorna None se o produto não tiver categoria (campo nullable).
        """
        if obj.categoria:
            return obj.categoria.nome
        return None

    # -------------------------------------------------------------------------
    # VALIDAÇÕES
    # -------------------------------------------------------------------------
    # Métodos validate_<campo> são chamados automaticamente pelo DRF
    # ao receber dados de POST/PUT/PATCH. Se levantar ValidationError,
    # o DRF retorna 400 Bad Request com a mensagem de erro.

    def validate_preco(self, value):
        """
        Validação de campo único: verifica apenas o campo 'preco'.
        Chamada automaticamente quando 'preco' está presente nos dados recebidos.
        """
        if value <= 0:
            raise serializers.ValidationError('O preço deve ser maior que zero.')
        return value  # sempre retorne o valor validado

    def validate_estoque(self, value):
        """
        Validação de campo único: verifica apenas o campo 'estoque'.
        """
        if value < 0:
            raise serializers.ValidationError('O estoque não pode ser negativo.')
        return value

    def validate(self, data):
        """
        Validação cruzada: acessa MÚLTIPLOS campos ao mesmo tempo.
        Chamada depois que cada campo individualmente já foi validado.

        Por que usar getattr aqui?
        Em atualizações parciais (PATCH), o cliente envia apenas os campos alterados.
        Se 'ativo' não foi enviado, pegamos o valor atual do objeto (self.instance).
        Se não há instância (criação via POST), usamos o valor padrão.
        """
        ativo = data.get('ativo', getattr(self.instance, 'ativo', True))
        estoque = data.get('estoque', getattr(self.instance, 'estoque', 0))

        # Regra de negócio: produto ativo precisa ter estoque disponível
        if ativo and estoque == 0:
            raise serializers.ValidationError(
                'Um produto ativo não pode ter estoque zero.'
            )
        return data  # sempre retorne o dicionário de dados validados


# =============================================================================
# JWT CUSTOMIZADO
# =============================================================================

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Estende o serializer padrão de login JWT para incluir dados extras no token.

    Um token JWT tem três partes: Header.Payload.Signature
    O Payload é um dicionário com informações. Por padrão, contém apenas
    user_id e dados de expiração. Aqui adicionamos username e email.

    Por que colocar dados no token?
    Permite que o frontend leia o nome do usuário sem fazer outra requisição.
    Decodifique em: https://jwt.io

    IMPORTANTE: NÃO coloque dados sensíveis (senha, cartão) no payload —
    ele é apenas codificado em Base64, não criptografado.
    """

    @classmethod
    def get_token(cls, user):
        # Chama o método pai para gerar o token padrão com campos obrigatórios
        token = super().get_token(user)

        # Adiciona campos extras ao payload do token
        # Esses dados ficam disponíveis para decodificação pelo cliente
        token['username'] = user.username
        token['email'] = user.email

        return token


# =============================================================================
# ITEM DE PEDIDO
# =============================================================================

class ItemPedidoSerializer(serializers.ModelSerializer):
    """
    Serializer para cada item dentro de um pedido.
    Mostra nome do produto e calcula o subtotal do item.
    """

    # source='produto.nome' = acessa o atributo 'nome' do objeto relacionado 'produto'.
    # É um atalho para evitar ter que criar um SerializerMethodField apenas para isso.
    # read_only=True pois é calculado — não faz sentido o cliente enviar.
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)

    # Campo calculado: quantidade × preço unitário
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItemPedido
        fields = ['id', 'produto', 'produto_nome', 'quantidade', 'preco_unitario', 'subtotal']

    def get_subtotal(self, obj):
        """Calcula o subtotal deste item: preço × quantidade."""
        # Convertemos Decimal para float para o JSON não reclamar de serialização
        return float(obj.preco_unitario) * obj.quantidade


# =============================================================================
# PEDIDO
# =============================================================================

class PedidoSerializer(serializers.ModelSerializer):
    """
    Serializer completo do pedido, incluindo todos os itens e o total.

    Relacionamento aninhado (nested): ao serializar um Pedido, o DRF também
    serializa automaticamente todos os itens relacionados via ItemPedidoSerializer.
    """

    # many=True = serializa uma lista de itens (queryset de ItemPedido)
    # read_only=True = itens são incluídos na resposta GET, mas não aceitos no POST
    # (itens são gerenciados separadamente)
    itens = ItemPedidoSerializer(many=True, read_only=True)

    # Total calculado em Python: soma de todos os subtotais dos itens
    total = serializers.SerializerMethodField()

    # source='cliente.username' = mostra o nome do usuário, não o ID numérico
    cliente_username = serializers.CharField(source='cliente.username', read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'cliente_username', 'criado_em', 'status', 'itens', 'total']
        read_only_fields = ['id', 'criado_em']

    def get_total(self, obj):
        """
        Itera sobre todos os itens do pedido e soma os subtotais.
        obj.itens.all() acessa a queryset de ItemPedido deste pedido
        via o related_name='itens' definido no model.
        """
        return sum(
            float(item.preco_unitario) * item.quantidade
            for item in obj.itens.all()
        )
