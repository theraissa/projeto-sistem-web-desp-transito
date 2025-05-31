import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(BASE_DIR, 'estrutura-logica'))

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from routes.cliente_cad import cad_cliente_bp
from routes.inicio_routes import inicio_bp

# --- FIXTURE CLIENTE --- #
@pytest.fixture
def client():
    """
    Fixture que configura o cliente de teste da aplicação Flask para o blueprint de cadastro de cliente.
    """
    test_app = Flask(__name__,
                     template_folder=os.path.join(BASE_DIR, 'interfaces'),
                     static_folder=os.path.join(BASE_DIR, 'interfaces'))
    test_app.config['TESTING'] = True
    test_app.secret_key = 'test_secret_cliente'

    test_app.register_blueprint(cad_cliente_bp, url_prefix='/cadastroCliente')
    test_app.register_blueprint(inicio_bp, url_prefix='/')

    with test_app.test_client() as client:
        yield client

# --- TESTES: /cadastro-cliente (POST) - cadastrar_cliente --- #
@patch('routes.cliente_cad.get_connection')
def test_cadastrar_cliente_post_ok(mock_get_conn, client):
    """
    Testa o cenário de sucesso para a rota /cadastroCliente/cadastro-cliente (POST).
    Verifica se o cliente é inserido no banco de dados e redireciona para a tela inicial.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.return_value = None
    mock_conn.commit.return_value = None
    mock_cursor.close.return_value = None
    mock_conn.close.return_value = None

    data = {
        'cpf-cliente': '12345678901',
        'nome-cliente': 'Cliente Teste',
        'email-cliente': 'cliente@teste.com',
        'senha-cliente': 'senha123',
        'confirmar-senha': 'senha123'
    }
    response = client.post('/cadastroCliente/cadastro-cliente', data=data)

    assert response.status_code == 302
    assert response.location == '/'
    with client.session_transaction() as sess:
        assert b'Cadastro realizado com sucesso!' in sess['_flashes'][0][1].encode('utf-8')
    mock_cursor.execute.assert_called_once_with(
        """
            INSERT INTO cliente (cpf_cliente, nome_cliente, email_cliente, senha_cliente)
            VALUES (%s, %s, %s, %s)""", ('12345678901', 'Cliente Teste', 'cliente@teste.com', 'senha123')
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()
