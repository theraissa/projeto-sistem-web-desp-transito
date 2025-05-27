from flask import Blueprint, render_template

cliente_bp = Blueprint('cliente', __name__)

# Se o login ocorrer tudo certo, será encaminhado para essa tela
@cliente_bp.route('/encontrarServicos')
def encon_desp_serv():
    return render_template('telas-cliente/encon-desp-serv/encon-desp-serv.html')

@cliente_bp.route('/chamadoCliente')
def chamado_cliente():
    return render_template('telas-cliente/chamado-cliente/chamado-cliente.html')

@cliente_bp.route('/perfilCliente')
def perfil_cliente():
    return render_template('telas-cliente/perfil-cliente/perfil-cliente.html')
