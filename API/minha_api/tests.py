from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal

from .models import Produto
from .serializers import ProdutoSerializer


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

class ProdutoModelTest(TestCase):

    def setUp(self):
        self.produto = Produto.objects.create(
            nome='Notebook',
            descricao='Notebook Dell',
            preco=Decimal('3500.00'),
            estoque=5,
        )

    def test_str_retorna_nome(self):
        self.assertEqual(str(self.produto), 'Notebook')

    def test_valores_default(self):
        p = Produto.objects.create(nome='Simples', preco=Decimal('10.00'))
        self.assertEqual(p.estoque, 0)
        self.assertTrue(p.ativo)
        self.assertEqual(p.descricao, '')

    def test_criado_em_preenchido_automaticamente(self):
        self.assertIsNotNone(self.produto.criado_em)


# ---------------------------------------------------------------------------
# Serializer
# ---------------------------------------------------------------------------

class ProdutoSerializerTest(TestCase):

    def test_dados_validos(self):
        data = {'nome': 'Mouse', 'preco': '99.90', 'estoque': 10}
        s = ProdutoSerializer(data=data)
        self.assertTrue(s.is_valid(), s.errors)

    def test_nome_obrigatorio(self):
        s = ProdutoSerializer(data={'preco': '50.00'})
        self.assertFalse(s.is_valid())
        self.assertIn('nome', s.errors)

    def test_preco_obrigatorio(self):
        s = ProdutoSerializer(data={'nome': 'Mouse'})
        self.assertFalse(s.is_valid())
        self.assertIn('preco', s.errors)

    def test_todos_campos_presentes(self):
        p = Produto.objects.create(nome='Teclado', preco=Decimal('150.00'))
        campos = set(ProdutoSerializer(p).data.keys())
        self.assertSetEqual(campos, {'id', 'nome', 'descricao', 'preco', 'estoque', 'ativo', 'criado_em'})

    def test_id_e_criado_em_sao_somente_leitura(self):
        meta = ProdutoSerializer.Meta
        self.assertIn('id', meta.read_only_fields)
        self.assertIn('criado_em', meta.read_only_fields)


# ---------------------------------------------------------------------------
# Autenticação JWT
# ---------------------------------------------------------------------------

class JWTAuthTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='senha123')

    def test_obter_token_com_credenciais_validas(self):
        r = self.client.post('/api/token/', {'username': 'teste', 'password': 'senha123'})
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertIn('access', r.data)
        self.assertIn('refresh', r.data)

    def test_credenciais_invalidas_retornam_401(self):
        r = self.client.post('/api/token/', {'username': 'teste', 'password': 'errada'})
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_gera_novo_access_token(self):
        r = self.client.post('/api/token/', {'username': 'teste', 'password': 'senha123'})
        r2 = self.client.post('/api/token/refresh/', {'refresh': r.data['refresh']})
        self.assertEqual(r2.status_code, status.HTTP_200_OK)
        self.assertIn('access', r2.data)

    def test_verify_token_valido(self):
        r = self.client.post('/api/token/', {'username': 'teste', 'password': 'senha123'})
        r2 = self.client.post('/api/token/verify/', {'token': r.data['access']})
        self.assertEqual(r2.status_code, status.HTTP_200_OK)

    def test_verify_token_invalido(self):
        r = self.client.post('/api/token/verify/', {'token': 'tokeninvalido'})
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)


# ---------------------------------------------------------------------------
# Permissões (sem autenticação)
# ---------------------------------------------------------------------------

class ProdutoPermissaoTest(APITestCase):

    def test_listar_sem_token_retorna_401(self):
        self.assertEqual(
            self.client.get('/api/produtos/').status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_criar_sem_token_retorna_401(self):
        self.assertEqual(
            self.client.post('/api/produtos/', {'nome': 'X', 'preco': '10.00'}).status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_detalhar_sem_token_retorna_401(self):
        p = Produto.objects.create(nome='P', preco=Decimal('1.00'))
        self.assertEqual(
            self.client.get(f'/api/produtos/{p.id}/').status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


# ---------------------------------------------------------------------------
# CRUD completo (autenticado)
# ---------------------------------------------------------------------------

class ProdutoViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='senha123')
        r = self.client.post('/api/token/', {'username': 'teste', 'password': 'senha123'})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {r.data["access"]}')

        self.produto = Produto.objects.create(
            nome='Monitor',
            descricao='Monitor 24"',
            preco=Decimal('1200.00'),
            estoque=3,
        )

    # LIST
    def test_listar_produtos_retorna_200(self):
        r = self.client.get('/api/produtos/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_listar_contem_produto_criado(self):
        r = self.client.get('/api/produtos/')
        itens = r.data.get('results', r.data)
        nomes = [p['nome'] for p in itens]
        self.assertIn('Monitor', nomes)

    # RETRIEVE
    def test_detalhar_produto_existente(self):
        r = self.client.get(f'/api/produtos/{self.produto.id}/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['nome'], 'Monitor')

    def test_detalhar_produto_inexistente_retorna_404(self):
        r = self.client.get('/api/produtos/9999/')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    # CREATE
    def test_criar_produto_valido(self):
        r = self.client.post('/api/produtos/', {'nome': 'Webcam', 'preco': '250.00', 'estoque': 10})
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Produto.objects.filter(nome='Webcam').exists())

    def test_criar_sem_nome_retorna_400(self):
        r = self.client.post('/api/produtos/', {'preco': '100.00'})
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nome', r.data)

    def test_criar_sem_preco_retorna_400(self):
        r = self.client.post('/api/produtos/', {'nome': 'Produto X'})
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('preco', r.data)

    def test_criar_ignora_id_informado(self):
        r = self.client.post('/api/produtos/', {'id': 999, 'nome': 'Headset', 'preco': '200.00'})
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(r.data['id'], 999)

    def test_criar_ignora_criado_em_informado(self):
        r = self.client.post('/api/produtos/', {
            'nome': 'Headset', 'preco': '200.00',
            'criado_em': '2000-01-01T00:00:00Z',
        })
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(r.data['criado_em'][:10], '2000-01-01')

    # UPDATE (PUT)
    def test_atualizar_produto_put(self):
        r = self.client.put(
            f'/api/produtos/{self.produto.id}/',
            {'nome': 'Monitor Full HD', 'preco': '1300.00', 'estoque': 5},
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.nome, 'Monitor Full HD')
        self.assertEqual(self.produto.preco, Decimal('1300.00'))

    def test_atualizar_produto_inexistente_retorna_404(self):
        r = self.client.put('/api/produtos/9999/', {'nome': 'X', 'preco': '1.00'})
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    # PARTIAL UPDATE (PATCH)
    def test_atualizar_parcial_estoque(self):
        r = self.client.patch(f'/api/produtos/{self.produto.id}/', {'estoque': 20})
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoque, 20)

    def test_atualizar_parcial_desativar_produto(self):
        r = self.client.patch(f'/api/produtos/{self.produto.id}/', {'ativo': False})
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.produto.refresh_from_db()
        self.assertFalse(self.produto.ativo)

    # DELETE
    def test_deletar_produto(self):
        r = self.client.delete(f'/api/produtos/{self.produto.id}/')
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Produto.objects.filter(id=self.produto.id).exists())

    def test_deletar_produto_inexistente_retorna_404(self):
        r = self.client.delete('/api/produtos/9999/')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
