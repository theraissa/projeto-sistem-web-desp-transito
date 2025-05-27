from flask import Flask
from routes.cliente_cad import cad_cliente_bp
from routes.cliente_func import cliente_bp
from routes.desp_cad import cad_desp_bp
from routes.desp_func import desp_bp
from routes.login_routes import login_bp
from routes.inicio_routes import inicio_bp

app = Flask(__name__,template_folder='../interfaces/', static_folder='../interfaces/')
app.secret_key = 'segredoSuperSecreto'

#tela de cadastro cliente
app.register_blueprint(cad_cliente_bp, url_prefix='/cadadastroCliente')
#telas cliente
app.register_blueprint(cliente_bp, url_prefix='/cliente')

#tela de cadastro despachante
app.register_blueprint(cad_desp_bp, url_prefix='/cadastroDespachante')
#telas despachante
app.register_blueprint(desp_bp, url_prefix='/despachante')

#tela para realizar o login
app.register_blueprint(login_bp, url_prefix='/login' )
#tela inicial do sistema
app.register_blueprint(inicio_bp)

if __name__ == '__main__':
    app.run(debug=True)
