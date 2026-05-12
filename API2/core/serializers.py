# serializers.py — Converte objetos Python (models) em JSON e vice-versa.
# Quando a API recebe um POST, o serializer valida os dados e salva no banco.
# Quando a API responde um GET, o serializer transforma o objeto em JSON.

from rest_framework import serializers
from .models import Categoria, Produto


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        # model diz de qual tabela este serializer vai ler/escrever dados.
        model = Categoria

        # fields lista quais colunas aparecem no JSON de resposta e entrada.
        fields = ['id', 'nome', 'descricao', 'ativa']

        # read_only_fields: o cliente não envia esses campos.
        # O id é gerado automaticamente pelo banco — não faz sentido o
        # cliente tentar definir ou alterar esse valor.
        read_only_fields = ['id']


class ProdutoSerializer(serializers.ModelSerializer):
    # Campo de saída (leitura): retorna o objeto completo da categoria.
    # read_only=True significa que este campo só aparece na resposta (GET).
    # Nunca é usado para receber dados do cliente.
    # Ao fazer GET /api/produtos/1/, a resposta terá:
    # "categoria": {"id": 1, "nome": "Eletrônicos", ...}
    categoria = CategoriaSerializer(read_only=True)

    # Campo de entrada (escrita): recebe apenas o ID da categoria.
    # write_only=True faz ele aparecer só na entrada (POST/PATCH), não na resposta.
    # source='categoria' diz ao DRF para gravar no atributo 'categoria' do model.
    # Sem isso o DRF procuraria um campo chamado exatamente 'categoria_id' que não existe.
    # allow_null=True e required=False permitem criar produtos sem categoria.
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source='categoria',
        write_only=True,
        allow_null=True,
        required=False,
    )

    # SerializerMethodField cria um campo calculado que não existe no banco.
    # O valor é gerado pelo método get_em_estoque() a cada requisição.
    # Útil para expor lógica de negócio sem criar coluna extra no banco.
    em_estoque = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'descricao', 'preco', 'estoque',
            'ativo', 'criado_em', 'categoria', 'categoria_id', 'em_estoque',
        ]
        # id: gerado pelo banco, não pode ser alterado pelo cliente.
        # criado_em: preenchido automaticamente com auto_now_add, também imutável.
        read_only_fields = ['id', 'criado_em']

    def get_em_estoque(self, obj):
        # O nome do método DEVE seguir o padrão get_<nome_do_campo>.
        # obj é a instância do Produto sendo serializado.
        # Retorna True se o estoque for maior que zero, False caso contrário.
        return obj.estoque > 0
