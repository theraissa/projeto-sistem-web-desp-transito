from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_connection

cad_desp_bp = Blueprint('cad_desp', __name__)

# Rota para exibir a tela de cadastro do despachante
@cad_desp_bp.route('/')
def tela_cadastro_despa():
    return render_template('telas-despachantes/cadastro-desp/cadastro-desp.html')

# Rota para processar o envio do formulário de cadastro
@cad_desp_bp.route('/cad-desp', methods=['POST'])
def cadastrar_desp():
    # Dados do Despachante
    nome_desp = request.form.get('nome_desp')
    cpf_desp = request.form.get('cpf_desp')
    rg_desp = request.form.get('rg_desp')
    nasc_desp = request.form.get('nasc_desp')
    tele_pessoal_desp = request.form.get('tele_pessoal_desp')
    email_desp = request.form.get('email_desp')
    senha_desp = request.form.get('senha_desp')
    confirmar_senha = request.form.get('senha_confir')
    regis_crdd = request.form.get('regis_crdd')
    data_exp_regis = request.form.get('data_exp_regis')
    
    # Dados do Estabelecimento
    tele_comercial = request.form.get('tele_comercial')
    endereco_desp = request.form.get('endereco_desp')
    num_desp = request.form.get('num_desp')
    bairro_desp = request.form.get('bairro_desp')
    cep_desp = request.form.get('cep_desp')
    cidade_desp = request.form.get('cidade_desp')
    estado_desp = request.form.get('estado_desp')
    
    if not all([nome_desp, cpf_desp, rg_desp, nasc_desp, tele_pessoal_desp, email_desp, senha_desp,
            regis_crdd, data_exp_regis, tele_comercial, endereco_desp, num_desp, bairro_desp,
            cep_desp, cidade_desp, estado_desp]) or senha_desp != confirmar_senha:
        flash("Por favor, preencha todos os campos obrigatórios.", "erro")
        return redirect(url_for('cad_desp.tela_cadastro_despa'))

    try:
        conn = get_connection()
        cur = conn.cursor()
         # Inserir na tabela Despachante
        cur.execute("""
            INSERT INTO despachante (
                cpf_desp, rg_desp, nome_desp, nasc_desp, tele_pessoal_desp, 
                email_desp, senha_desp, regis_crdd, data_exp_regis
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (cpf_desp, rg_desp, nome_desp, nasc_desp, tele_pessoal_desp, 
              email_desp, senha_desp, regis_crdd, data_exp_regis))

        # Inserir na tabela Estabelecimento
        cur.execute("""
            INSERT INTO estabelecimento (
                cpf_desp, tele_comercial, endereco_desp, num_desp, 
                bairro_desp, cep_desp, cidade_desp, estado_desp
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (cpf_desp, tele_comercial, endereco_desp, num_desp, 
              bairro_desp, cep_desp, cidade_desp, estado_desp))
        
        conn.commit()
        cur.close()
        conn.close()
        
        flash("Despachante cadastrado com sucesso!", "sucesso")
        return redirect(url_for('inicio.tela_inicial'))
    
    except Exception as e:
        flash(f"Erro ao cadastrar: {str(e)}", "erro")
        return redirect(url_for('cad_desp.tela_cadastro_despa'))
