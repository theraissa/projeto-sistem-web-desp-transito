from flask import Blueprint, render_template

inicio_bp = Blueprint('inicio', __name__)

@inicio_bp.route('/')
def index():
    return render_template('index.html')

#Tela onde você vai escolher o tipo de cadastro, como cliente ou despachante
@inicio_bp.route('/cliente_desp')
def cad_cliente_desp():
    return render_template('cliente-desp/cliente-desp.html')