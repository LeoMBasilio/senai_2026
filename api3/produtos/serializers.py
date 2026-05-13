from rest_framework import serializers
from .models import Categoria, Produto, Pedido, ItemPedido


# --- Aula 3 - Ex 5: CategoriaSerializer ---
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'
        read_only_fields = ['id']


# --- Aula 3 - Ex 5: ProdutoSerializer com nome da categoria ---
class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = '__all__'
        read_only_fields = ['id', 'criado_em']

    def get_categoria_nome(self, obj):
        if obj.categoria:
            return obj.categoria.nome
        return None

    # --- Aula 3 - Ex 6: validações ---
    def validate_preco(self, value):
        if value <= 0:
            raise serializers.ValidationError('O preço deve ser maior que zero.')
        return value

    def validate_estoque(self, value):
        if value < 0:
            raise serializers.ValidationError('O estoque não pode ser negativo.')
        return value

    def validate(self, data):
        ativo = data.get('ativo', getattr(self.instance, 'ativo', True))
        estoque = data.get('estoque', getattr(self.instance, 'estoque', 0))
        if ativo and estoque == 0:
            raise serializers.ValidationError(
                'Um produto ativo não pode ter estoque zero.'
            )
        return data


# --- Aula 5 - Ex 6: JWT customizado (serializer de autenticação) ---
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token


# --- Aula 3 - Desafio 7: PedidoSerializer com total calculado ---
class ItemPedidoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItemPedido
        fields = ['id', 'produto', 'produto_nome', 'quantidade', 'preco_unitario', 'subtotal']

    def get_subtotal(self, obj):
        return float(obj.preco_unitario) * obj.quantidade


class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    cliente_username = serializers.CharField(source='cliente.username', read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'cliente_username', 'criado_em', 'status', 'itens', 'total']
        read_only_fields = ['id', 'criado_em']

    def get_total(self, obj):
        return sum(
            float(item.preco_unitario) * item.quantidade
            for item in obj.itens.all()
        )
