from flask import Blueprint, request, render_template, redirect, url_for, flash
from db import get_connection

cad_cliente_bp = Blueprint('cad_cliente', __name__)

@cad_cliente_bp.route('/')
def tela_cadastro():
    return render_template('telas-cliente/cadastro-cliente/cadastro-cliente.html')

@cad_cliente_bp.route('/cadastro-cliente', methods=['POST'])
def cadastrar_cliente():
    cpf = request.form.get('cpf-cliente')
    nome = request.form.get('nome-cliente')
    email = request.form.get('email-cliente')
    senha = request.form.get('senha-cliente')
    confirmar_senha = request.form.get('confirmar-senha')

    if not all([cpf, nome, email, senha]) or senha != confirmar_senha:
        flash("Preencha todos os campos corretamente.", "erro")
        return redirect(url_for('cad_cliente.tela_cadastro'))
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO cliente (cpf_cliente, nome_cliente, email_cliente, senha_cliente)
            VALUES (%s, %s, %s, %s)""", (cpf, nome, email, senha))

        conn.commit()
        cur.close()
        conn.close()
        flash("Cadastro realizado com sucesso! Faça login para continuar.")
        return redirect(url_for('inicio.tela_inicial'))
    
    except Exception as e:
        flash(f"Ocorreu um erro: {str(e)}", "erro")
        return redirect(url_for('cad_cliente.tela_cadastro'))
