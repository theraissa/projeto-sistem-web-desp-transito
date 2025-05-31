import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(BASE_DIR, 'estrutura-logica'))

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from routes.desp_cad import cad_desp_bp
from routes.inicio_routes import inicio_bp

# --- FIXTURE CLIENTE --- #
@pytest.fixture
def client():
    """
    Fixture que configura o cliente de teste da aplicação Flask para o blueprint de cadastro.
    Cria uma nova instância da aplicação Flask para cada teste.
    """
    test_app = Flask(__name__,
                     template_folder=os.path.join(BASE_DIR, 'interfaces'),
                     static_folder=os.path.join(BASE_DIR, 'interfaces'))
    test_app.config['TESTING'] = True
    test_app.secret_key = 'test_secret_cad'
    test_app.register_blueprint(cad_desp_bp, url_prefix='/cadastroDespachante')
    test_app.register_blueprint(inicio_bp, url_prefix='/')

    with test_app.test_client() as client:
        yield client

# --- TESTES: /cad-desp (POST) - cadastrar_desp --- #
@patch('routes.desp_cad.get_connection')
def test_cadastrar_desp_post_ok(mock_get_conn, client):
    """
    Testa o cenário de sucesso para a rota /cadastroDespachante/cad-desp (POST).
    Verifica se o despachante e estabelecimento são inseridos e redireciona com sucesso.
    """
    mock_cursor = MagicMock()
    mock_get_conn.return_value.cursor.return_value = mock_cursor
    mock_get_conn.return_value.close.return_value = None
    mock_cursor.close.return_value = None
    mock_get_conn.return_value.commit.return_value = None

    data = {
        'nome_desp': 'Novo Despachante',
        'cpf_desp': '11122233344',
        'rg_desp': '1234567',
        'nasc_desp': '1990-01-01',
        'tele_pessoal_desp': '999999999',
        'email_desp': 'novo.desp@email.com',
        'senha_desp': 'senha_segura',
        'senha_confir': 'senha_segura',
        'regis_crdd': 'CRDD-ABC',
        'data_exp_regis': '2025-12-31',
        'tele_comercial': '888888888',
        'endereco_desp': 'Rua Nova',
        'num_desp': '50',
        'bairro_desp': 'Centro',
        'cep_desp': '00000-000',
        'cidade_desp': 'Cidade Teste',
        'estado_desp': 'TS'
    }

    response = client.post('/cadastroDespachante/cad-desp', data=data)

    assert response.status_code == 302 
    assert response.location == '/' 
    with client.session_transaction() as sess:
        assert b'Despachante cadastrado com sucesso!' in sess['_flashes'][0][1].encode('utf-8')
    
    mock_cursor.execute.assert_called()
    mock_get_conn.return_value.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_get_conn.return_value.close.assert_called_once()