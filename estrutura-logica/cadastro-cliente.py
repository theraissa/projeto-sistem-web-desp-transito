from flask import Flask, render_template, request, send_from_directory
import os

# Define caminhos personalizados
template_dir = os.path.abspath('../interfaces/telas-cliente/cadastro-cliente/cadastro-cliente.html')
static_dir = os.path.abspath('../interfaces/telas-cliente/cadastro-cliente/cadastro-cliente.html')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

@app.route('/')
def index():
    return render_template('cadastro-cliente.html')

@app.route('/cadastro', methods=['POST'])
def cadastrar_cliente():
    nome = request.form['nome']
    # ... (demais campos)
    return f"Cadastro recebido: {nome}"

# Se quiser servir arquivos estáticos manualmente
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(static_dir, filename)

if __name__ == '__main__':
    app.run(debug=True)
