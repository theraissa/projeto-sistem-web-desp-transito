from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_connection

cad_desp_bp = Blueprint('cad_desp', __name__)

# Rota para exibir a tela de cadastro do despachante
@cad_desp_bp.route('/')
def tela_cadastro_despachante():
    return render_template('telas-despachantes/cadastro-desp/cadastro-desp.html')

# Rota para processar o envio do formulário de cadastro
@cad_desp_bp.route('/cad-desp', methods=['POST'])
def cadastrar_despachante():
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    rg = request.form.get('rg')
    data_nasc = request.form.get('data_nasc')
    telefone_pessoal = request.form.get('telefone_pessoal')
    telefone_comercial = request.form.get('telefone_comercial')
    email = request.form.get('email')
    senha = request.form.get('senha')
    crdd = request.form.get('crdd')
    data_expiracao = request.form.get('data_expiracao')
    endereco = request.form.get('endereco')
    bairro = request.form.get('bairro')
    cep = request.form.get('cep')
    cidade = request.form.get('cidade')
    estado = request.form.get('estado')

    # Verificação simples de preenchimento
    if not nome or not cpf or not email or not senha:
        flash("Por favor, preencha os campos obrigatórios.", "erro")
        return redirect(url_for('cad_desp.tela_cadastro_despachante'))

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO despachante (
                nome, cpf, rg, data_nasc, telefone_pessoal, telefone_comercial, 
                email, senha, crdd, data_expiracao, endereco, bairro, cep, cidade, estado
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            nome, cpf, rg, data_nasc, telefone_pessoal, telefone_comercial, 
            email, senha, crdd, data_expiracao, endereco, bairro, cep, cidade, estado
        ))
        conn.commit()
        cur.close()
        conn.close()
        
        flash("Despachante cadastrado com sucesso!", "sucesso")
        return redirect(url_for('cad_desp.tela_cadastro_despachante'))
    
    except Exception as e:
        flash(f"Erro ao cadastrar: {str(e)}", "erro")
        return redirect(url_for('cad_desp.tela_cadastro_despachante'))
