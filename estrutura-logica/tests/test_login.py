import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(BASE_DIR, 'estrutura-logica'))

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, session
from routes.login_routes import login_bp
from db import get_connection
from routes.cliente_func import cliente_bp  # Importe para usar url_for
from routes.desp_func import desp_bp # Importe para usar url_for

# --- FIXTURE CLIENTE --- #
@pytest.fixture
def client():
    """
    Fixture que configura o cliente de teste da aplicação Flask para o blueprint de login.
    """
    test_app = Flask(__name__,
                     template_folder=os.path.join(BASE_DIR, 'interfaces'),
                     static_folder=os.path.join(BASE_DIR, 'interfaces'))
    test_app.config['TESTING'] = True
    test_app.secret_key = 'test_secret_login'

    test_app.register_blueprint(login_bp, url_prefix='/login')
    test_app.register_blueprint(cliente_bp, url_prefix='/cliente')
    test_app.register_blueprint(desp_bp, url_prefix='/despachante')

    with test_app.test_client() as client:
        yield client

# --- TESTES: /login/ (GET) - tela_login --- #
def test_tela_login_get_ok(client):
    """
    Testa o cenário de sucesso para a rota /login/ (GET).
    Verifica se a página de login é carregada com status 200.
    """
    response = client.get('/login/')
    assert response.status_code == 200
    assert b'Login' in response.data

# --- TESTES: /login/login (POST) - login --- #
@patch('routes.login_routes.get_connection')
def test_login_post_cliente_sucesso(mock_get_conn, client):
    """
    Testa o login bem-sucedido de um cliente.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.side_effect = [('cliente_cpf', 'Cliente Nome'), None]
    mock_cursor.close.return_value = None
    mock_conn.close.return_value = None

    data = {'email-cliente': 'cliente@email.com', 'senha-cliente': 'senha123'}
    response = client.post('/login/login', data=data, follow_redirects=False)

    assert response.status_code == 302
    assert response.location == '/cliente/encontrarServicos'
    with client.session_transaction() as sess:
        assert sess['cliente_id'] == 'cliente_cpf'
        assert sess['cliente_nome'] == 'Cliente Nome'
        assert 'desp_id' not in sess
        assert 'desp_nome' not in sess
    mock_cursor.execute.assert_any_call(
        "SELECT cpf_cliente, nome_cliente FROM cliente WHERE email_cliente = %s AND senha_cliente = %s",
        ('cliente@email.com', 'senha123')
    )
    
@patch('routes.login_routes.get_connection')
def test_login_post_despachante_sucesso(mock_get_conn, client):
    """
    Testa o login bem-sucedido de um despachante.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.side_effect = [None, ('desp_cpf', 'Despachante Nome')]
    mock_cursor.close.return_value = None
    mock_conn.close.return_value = None

    data = {'email-cliente': 'desp@email.com', 'senha-cliente': 'senha456'}
    response = client.post('/login/login', data=data, follow_redirects=False)

    assert response.status_code == 302
    assert response.location == '/despachante/servicos'
    with client.session_transaction() as sess:
        assert sess['desp_id'] == 'desp_cpf'
        assert sess['desp_nome'] == 'Despachante Nome'
        assert 'cliente_id' not in sess
        assert 'cliente_nome' not in sess

    mock_cursor.execute.assert_any_call(
        "SELECT cpf_desp, nome_desp FROM despachante WHERE email_desp = %s AND senha_desp = %s",
        ('desp@email.com', 'senha456')
    )

@patch('routes.login_routes.get_connection')
def test_login_post_falha_credenciais_invalidas(mock_get_conn, client):
    """
    Testa o login com credenciais inválidas.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None # Simula nenhum usuário encontrado
    mock_cursor.close.return_value = None
    mock_conn.close.return_value = None

    data = {'email-cliente': 'usuario@email.com', 'senha-cliente': 'senha_errada'}
    response = client.post('/login/login', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'Email ou senha incorretos.' in response.data
    
# --- TESTES: /login/logout (GET) - logout --- #
def test_logout_get_ok(client):
    """
    Testa a funcionalidade de logout.
    """
    with client.session_transaction() as sess:
        sess['cliente_id'] = 'algum_id'
        sess['cliente_nome'] = 'Algum Nome'
        sess['desp_id'] = 'algum_desp_id'
        sess['desp_nome'] = 'Algum Despachante'

    response = client.get('/login/logout', follow_redirects=True)
    assert response.status_code == 200
    assert 'Você saiu da sua conta.' in response.get_data(as_text=True)

    with client.session_transaction() as sess:
        assert 'cliente_id' not in sess
        assert 'cliente_nome' not in sess
        assert 'desp_id' not in sess
        assert 'desp_nome' not in sess