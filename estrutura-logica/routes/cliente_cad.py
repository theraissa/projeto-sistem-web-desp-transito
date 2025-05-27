from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash
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
    senha_hash = generate_password_hash(senha)

    confirmar_senha = request.form.get('confirmar-senha')

    if not cpf or not nome or not email or not senha or senha != confirmar_senha:
        flash("Preencha todos os campos corretamente.", "erro")
        return redirect(url_for('cad_cliente.tela_cadastro'))

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO cliente (cpf_cliente, nome_cliente, email_cliente, senha_cliente)
            VALUES (%s, %s, %s, %s)
        """, (cpf, nome, email, senha_hash))
        conn.commit()
        cur.close()
        conn.close()
        flash("Cadastro realizado com sucesso! Faça login para continuar.")
        return redirect(url_for('login.tela_login'))
    
    except Exception as e:
        flash(f"Ocorreu um erro: {str(e)}", "erro")
        return redirect(url_for('cad_cliente.tela_cadastro'))
