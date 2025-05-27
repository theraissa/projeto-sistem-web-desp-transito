from flask import Blueprint, render_template

desp_bp = Blueprint('despachante', __name__)

# Se o login ocorrer tudo certo, será encaminhado para essa tela
@desp_bp.route('/servicos')
def servico_desp():
    return render_template('telas-despachantes/servico-desp/servico-desp.html')

@desp_bp.route('/chamados')
def chamado_desp():
    return render_template('telas-despachantes/chamado-desp/chamado-desp.html')

@desp_bp.route('/agendamentos')
def agenda_desp():
    return render_template('telas-despachantes/agend-desp/agend-desp.html')

@desp_bp.route('/perfil')
def perfil_desp():
    return render_template('telas-despachantes/perfil-desp/perfil-desp.html')