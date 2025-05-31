import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(BASE_DIR, 'estrutura-logica'))

import pytest
from flask import Flask

from routes.inicio_routes import inicio_bp

# --- FIXTURE CLIENTE --- #
@pytest.fixture
def client():
    """
    Fixture que configura o cliente de teste da aplicação Flask para o blueprint de início.
    """
    test_app = Flask(__name__,
                     template_folder=os.path.join(BASE_DIR, 'interfaces'),
                     static_folder=os.path.join(BASE_DIR, 'interfaces'))
    test_app.config['TESTING'] = True
    test_app.secret_key = 'test_secret_inicio'

    test_app.register_blueprint(inicio_bp, url_prefix='/')

    with test_app.test_client() as client:
        yield client

# --- TESTES: / (GET) - tela_inicial --- #
def test_tela_inicial_get_ok(client):
    """
    Testa o cenário de sucesso para a rota / (GET).
    Verifica se a página inicial é carregada com status 200.
    """
    response = client.get('/')
    assert response.status_code == 200

# --- TESTES: /cliente_desp (GET) - cad_cliente_desp --- #
def test_cad_cliente_desp_get_ok(client):
    """
    Testa o cenário de sucesso para a rota /cliente_desp (GET).
    Verifica se a página de escolha de cadastro é carregada com status 200.
    """
    response = client.get('/cliente_desp')
    assert response.status_code == 200
    assert b'Cliente' in response.data
    assert b'Despachante' in response.data