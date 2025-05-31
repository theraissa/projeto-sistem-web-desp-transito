import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(BASE_DIR, 'estrutura-logica'))

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask 
from routes.desp_func import desp_bp
from routes.login_routes import login_bp

# --- FIXTURE CLIENTE --- #
@pytest.fixture
def client():
    """
    Fixture que configura o cliente de teste da aplicação Flask.
    Cria uma nova instância da aplicação Flask para cada teste,
    evitando o erro de blueprint já registrado e garantindo o caminho correto das templates.
    """
    # Cria uma nova instância do Flask para o teste
    test_app = Flask(__name__,
                     template_folder=os.path.join(BASE_DIR, 'interfaces'), 
                     static_folder=os.path.join(BASE_DIR, 'interfaces')) 
    test_app.config['TESTING'] = True
    test_app.secret_key = 'test_secret'

    # Registra os blueprints necessários para os testes
    # O url_prefix é importante para que as rotas sejam acessadas corretamente nos testes
    test_app.register_blueprint(desp_bp, url_prefix='/despachante')
    test_app.register_blueprint(login_bp, url_prefix='/login')

    with test_app.test_client() as client:
        yield client

# --- FIXTURE LOGIN SESSION --- #
@pytest.fixture
def login_session(client):
    """
    Fixture que simula uma sessão de usuário logado.
    Define 'desp_id' na sessão para simular o login de um despachante.
    """
    with client.session_transaction() as sess:
        sess['desp_id'] = '12345678900'
    yield

# --- TESTE: /servicos (GET) --- #
@patch('routes.desp_func.get_connection')  # O patch é necessário mesmo que não use o DB para consistência
def test_servico_desp_ok(mock_get_conn, client, login_session):
    """
    Testa o cenário de sucesso para a rota /despachante/servicos.
    Verifica se a página é carregada com status 200 e exibe os serviços mockados.
    """
    # Mock do cursor e da conexão do banco de dados
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(1, 'CNH'), (2, 'Placa')] # Retorna serviços mockados
    mock_get_conn.return_value.cursor.return_value = mock_cursor
    mock_get_conn.return_value.close.return_value = None # Mock para o método close da conexão
    mock_cursor.close.return_value = None # Mock para o método close do cursor

    response = client.get('/despachante/servicos') # Faz a requisição GET para a rota

    assert response.status_code == 200 
    assert b'Ol\xc3\xa1, Nome Despachante' in response.data
    assert b'Adicionar Servi\xc3\xa7o' in response.data
    assert b'CNH' in response.data 
    assert b'Placa' in response.data
    assert b'Voc\xc3\xaa ainda n\xc3\xa3o cadastrou nenhum servi\xc3\xa7o.' not in response.data
    
    # Verifica se a consulta SQL foi executada (simplificado para não exigir correspondência exata da string)
    mock_cursor.execute.assert_called_once() # Apenas verifica se 'execute' foi chamado uma vez
    mock_cursor.close.assert_called_once() # Verifica se o cursor foi fechado
    mock_get_conn.return_value.close.assert_called_once() # Verifica se a conexão foi fechada

# --- TESTE: /criarNovoServico (GET) --- #
@patch('routes.desp_func.get_connection')
def test_criar_servico_get_ok(mock_get_conn, client, login_session):
    """
    Testa o cenário de sucesso para a rota /despachante/criarNovoServico (GET).
    Verifica se a página de criação de serviço é carregada com status 200.
    """
    response = client.get('/despachante/criarNovoServico')

    assert response.status_code == 200 
    assert b'Criar Novo Servi\xc3\xa7o' in response.data
    mock_get_conn.assert_not_called()

# --- TESTES: /criarNovoServico (POST) --- #
@patch('routes.desp_func.get_connection')
def test_criar_servico_post_ok(mock_get_conn, client, login_session):
    """
    Testa o cenário de sucesso para a rota /despachante/criarNovoServico (POST).
    Verifica se o serviço e documentos são inseridos e redireciona com sucesso.
    """
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (100,)
    mock_get_conn.return_value.cursor.return_value = mock_cursor
    mock_get_conn.return_value.close.return_value = None
    mock_cursor.close.return_value = None
    mock_get_conn.return_value.commit.return_value = None
    
    data = {
        'nome_servico': 'Servico Teste Basico',
        'documento[]': ['Doc Simples 1', 'Doc Simples 2']
    }
    response = client.post('/despachante/criarNovoServico', data=data)

    assert response.status_code == 302
    assert response.location == '/despachante/servicos'
    # Verifica a mensagem flash de sucesso (Flask armazena em _flashes na sessão)
    with client.session_transaction() as sess:
        assert b'Servi\xc3\xa7o e documentos criados com sucesso!' in sess['_flashes'][0][1].encode('utf-8')

    mock_cursor.execute.assert_called() 
    mock_get_conn.return_value.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_get_conn.return_value.close.assert_called_once()

# --- TESTES: /deletarServico (POST) --- #
@patch('routes.desp_func.get_connection')
def test_deletar_servico_post_ok(mock_get_conn, client, login_session):
    """
    Testa o cenário de sucesso para a rota /deletarServico (POST).
    Verifica se o serviço e seus documentos são deletados e redireciona com sucesso.
    """
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)
    mock_get_conn.return_value.cursor.return_value = mock_cursor
    mock_get_conn.return_value.close.return_value = None
    mock_cursor.close.return_value = None
    mock_get_conn.return_value.commit.return_value = None

    data = {'id_servico': '1'}
    response = client.post('/despachante/deletarServico', data=data)

    assert response.status_code == 302 
    assert response.location == '/despachante/servicos' 
    # Verifica a mensagem flash de sucesso
    with client.session_transaction() as sess:
        assert b'Servi\xc3\xa7o exclu\xc3\xaddo com sucesso.' in sess['_flashes'][0][1].encode('utf-8')
    
    mock_cursor.execute.assert_called() 
    mock_get_conn.return_value.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_get_conn.return_value.close.assert_called_once()


# --- TESTES: /editarServico (GET) --- #
@patch('routes.desp_func.get_connection')
def test_editar_servico_get_ok(mock_get_conn, client, login_session):
    """
    Testa o cenário de sucesso para a rota /despachante/editarServico (GET).
    Verifica se a página de edição é carregada com status 200 e exibe os dados do serviço.
    """
    mock_cursor = MagicMock()
    mock_cursor.fetchone.side_effect = [(1, 'Servico Existente')] # Para a primeira fetchone (serviço)
    mock_cursor.fetchall.return_value = [(101, 'Doc Existente 1'), (102, 'Doc Existente 2')] # Para a fetchall (documentos)
    mock_get_conn.return_value.cursor.return_value = mock_cursor
    mock_get_conn.return_value.close.return_value = None
    mock_cursor.close.return_value = None

    data = {'id_servico': '1'}
    response = client.post('/despachante/editarServico', data=data)

    assert response.status_code == 200 
    assert b'Editar Servi\xc3\xa7o' in response.data 
    assert b'Servico Existente' in response.data 
    assert b'Doc Existente 1' in response.data
    assert b'Doc Existente 2' in response.data 
    mock_cursor.execute.assert_called() 
    mock_cursor.close.assert_called_once()
    mock_get_conn.return_value.close.assert_called_once()

# --- TESTES: /atualizarServico (POST) --- #
@patch('routes.desp_func.get_connection')
def test_atualizar_servico_post_ok(mock_get_conn, client, login_session):
    """
    Testa o cenário de sucesso para a rota /despachante/atualizarServico (POST).
    Verifica se o serviço e documentos são atualizados e redireciona com sucesso.
    """
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)
    mock_get_conn.return_value.cursor.return_value = mock_cursor
    mock_get_conn.return_value.close.return_value = None
    mock_cursor.close.return_value = None
    mock_get_conn.return_value.commit.return_value = None 
    data = {
        'id_servico': '1',
        'nome_servico': 'Servico Atualizado',
        'documento[]': ['Doc Atualizado 1', 'Doc Atualizado 2']
    }

    response = client.post('/despachante/atualizarServico', data=data)

    assert response.status_code == 302 
    assert response.location == '/despachante/servicos'
    with client.session_transaction() as sess:
        assert b'Servi\xc3\xa7o atualizado com sucesso!' in sess['_flashes'][0][1].encode('utf-8')
    
    mock_cursor.execute.assert_called() 
    mock_get_conn.return_value.commit.assert_called_once() 
    mock_cursor.close.assert_called_once()
    mock_get_conn.return_value.close.assert_called_once()


# --- TESTES: /chamados (GET) --- #
@patch('routes.desp_func.get_connection')
def test_chamado_desp_get_ok(mock_get_conn, client, login_session):
    """
    Testa o cenário de sucesso para a rota /despachante/chamados (GET).
    Verifica se a página é carregada com status 200.
    """
    response = client.get('/despachante/chamados')
    assert response.status_code == 200 
    mock_get_conn.assert_not_called() 

# --- TESTES: /agendamentos (GET) --- #
@patch('routes.desp_func.get_connection')
def test_agenda_desp_get_ok(mock_get_conn, client, login_session):
    """
    Testa o cenário de sucesso para a rota /despachante/agendamentos (GET).
    Verifica se a página é carregada com status 200.
    """
    response = client.get('/despachante/agendamentos')
    assert response.status_code == 200
    mock_get_conn.assert_not_called()

# --- TESTES: /perfil (GET) --- #
@patch('routes.desp_func.get_connection')
def test_perfil_desp_get_ok(mock_get_conn, client, login_session):
    """
    Testa o cenário de sucesso para a rota /despachante/perfil (GET).
    Verifica se a página é carregada com status 200 e exibe os dados do despachante e estabelecimento.
    """
    mock_cursor = MagicMock()
    mock_cursor.fetchone.side_effect = [
        ('12345678900', 'Nome Despachante', '1234567', '1990-01-01', '999999999', 'desp@email.com', 'senha123', 'CRDD123', '2025-12-31'),
        (1, '12345678900','999999999' ,'Rua A', '100', 'Bairro B', '12345678', 'Cidade C', 'Estado D') # Estabelecimento
    ]
    mock_get_conn.return_value.cursor.return_value = mock_cursor
    mock_get_conn.return_value.close.return_value = None
    mock_cursor.close.return_value = None

    response = client.get('/despachante/perfil')
    assert response.status_code == 200
    assert b'Nome Despachante' in response.data
    assert b'Rua A' in response.data    
    mock_cursor.execute.assert_called()
    mock_cursor.close.assert_called_once()
    mock_get_conn.return_value.close.assert_called_once()


# --- TESTES: /perfil (POST) - atualizar_perfil_desp --- #
@patch('routes.desp_func.get_connection')
def test_atualizar_perfil_desp_post_ok(mock_get_conn, client, login_session):
    """
    Testa o cenário de sucesso para a rota /despachante/perfil (POST).
    Verifica se os dados do despachante e estabelecimento são atualizados e redireciona com sucesso.
    """
    mock_cursor = MagicMock()
    mock_get_conn.return_value.cursor.return_value = mock_cursor
    mock_get_conn.return_value.close.return_value = None
    mock_cursor.close.return_value = None
    mock_get_conn.return_value.commit.return_value = None

    data = {
        'nome_desp': 'Nome Despachante Atualizado',
        'cpf_desp': '12345678900',
        'rg_desp': '1234567',
        'nasc_desp': '1990-01-01',
        'tele_pessoal_desp': '999999999',
        'email_desp': 'desp_atualizado@email.com',
        'senha_desp': 'nova_senha',
        'senha_confir': 'nova_senha',
        'regis_crdd': 'CRDD456',
        'data_exp_regis': '2026-12-31',
        'tele_comercial': '888888888',
        'endereco_desp': 'Rua B',
        'num_desp': '200',
        'bairro_desp': 'Bairro C',
        'cep_desp': '98765-432',
        'cidade_desp': 'Cidade D',
        'estado_desp': 'Estado E'
    }

    response = client.post('/despachante/perfil', data=data)
    assert response.status_code == 302 
    assert response.location == '/despachante/perfil' 
    with client.session_transaction() as sess:
        assert b'Perfil atualizado com sucesso!' in sess['_flashes'][0][1].encode('utf-8')
    
    mock_cursor.execute.assert_called() 
    mock_get_conn.return_value.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_get_conn.return_value.close.assert_called_once()
    