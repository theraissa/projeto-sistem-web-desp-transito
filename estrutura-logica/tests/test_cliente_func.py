import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(BASE_DIR, 'estrutura-logica'))

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, session
from routes.cliente_func import cliente_bp
from routes.login_routes import login_bp 
from routes.inicio_routes import inicio_bp

# --- FIXTURE CLIENTE --- #
@pytest.fixture
def client():
    """
    Fixture que configura o cliente de teste da aplicação Flask para o blueprint de cliente.
    """
    test_app = Flask(__name__,
                     template_folder=os.path.join(BASE_DIR, 'interfaces'),
                     static_folder=os.path.join(BASE_DIR, 'interfaces'))
    test_app.config['TESTING'] = True
    test_app.secret_key = 'test_secret_cliente_routes'

    test_app.register_blueprint(cliente_bp, url_prefix='/cliente')
    test_app.register_blueprint(login_bp, url_prefix='/login')
    test_app.register_blueprint(inicio_bp, url_prefix='/')

    with test_app.test_client() as client:
        with client.session_transaction() as sess:
            sess['cliente_id'] = 'test_cpf'
        yield client

# --- TESTES: /cliente/encontrarServicos (GET) --- #
@patch('routes.cliente_func.get_connection')
def test_encon_desp_serv_get_logado(mock_get_conn, client):
    """
    Testa a rota /cliente/encontrarServicos quando o cliente está logado.
    Verifica se a página é carregada e se a busca por despachantes funciona.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('cpf1', 'nome1', 'rg1', '...')]
    mock_cursor.close.return_value = None
    mock_conn.close.return_value = None

    response = client.get('/cliente/encontrarServicos')
    assert response.status_code == 200
    mock_cursor.execute.assert_called()

# --- TESTES: /cliente/chamadoCliente (GET) --- #
def test_chamado_cliente_get_logado(client):
    """
    Testa a rota /cliente/chamadoCliente quando o cliente está logado.
    """
    response = client.get('/cliente/chamadoCliente')
    assert response.status_code == 200

# --- TESTES: /cliente/perfilCliente (GET) --- #
@patch('routes.cliente_func.get_connection')
def test_perfil_cliente_get_logado(mock_get_conn, client):
    """
    Testa a rota /cliente/perfilCliente quando o cliente está logado.
    Verifica se os dados do cliente e endereço são carregados.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.side_effect = [
        ('test_cpf', 'Nome Teste', 'email@teste.com', 'senha_hash'),
        ('test_cpf', 'telefone', 'endereco', 'num', 'bairro', 'cep', 'cidade', 'estado')
    ]
    mock_cursor.close.return_value = None
    mock_conn.close.return_value = None

    response = client.get('/cliente/perfilCliente')
    assert response.status_code == 200
    assert b'Nome Teste' in response.data
    assert b'endereco' in response.data
    mock_cursor.execute.assert_any_call("SELECT * FROM cliente WHERE cpf_cliente = %s", ('test_cpf',))
    mock_cursor.execute.assert_any_call("SELECT * FROM endereco WHERE cpf_cliente = %s", ('test_cpf',))
    
# --- TESTES: /cliente/perfilCliente (POST) --- #
@patch('routes.cliente_func.get_connection')
def test_atualizar_perfil_cliente_post_logado_sucesso(mock_get_conn, client):
    """
    Testa a atualização do perfil do cliente logado com dados válidos.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = ('test_cpf',)
    mock_conn.commit.return_value = None
    mock_cursor.close.return_value = None
    mock_conn.close.return_value = None

    data = {
        'nome_cliente': 'Novo Nome',
        'cpf_cliente': 'test_cpf',
        'rg_cliente': 'novo_rg',
        'nasc_cliente': '2000-01-01',
        'tele_pessoal_cliente': '111111111',
        'email_cliente': 'novo@email.com',
        'senha_cliente': 'nova_senha',
        'senha_confir': 'nova_senha',
        'tele_residencial': '222222222',
        'endereco_cliente': 'Novo Endereco',
        'num_cliente': '100',
        'bairro_cliente': 'Novo Bairro',
        'cep_cliente': '00000000',
        'cidade_cliente': 'Nova Cidade',
        'estado_cliente': 'NC'
    }
    response = client.post('/cliente/perfilCliente', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Perfil atualizado com sucesso!' in response.data
    mock_conn.commit.assert_called_once()