from flask import Blueprint, request, render_template, redirect, url_for, flash
from db import get_connection

login_bp = Blueprint('login', __name__)

@login_bp.route('/')
def tela_login():
    return render_template('login/login.html')

# Rota de login
@login_bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email-cliente')
    senha = request.form.get('senha-cliente')

    if not email or not senha:
        flash("Preencha todos os campos.", "erro")
        return redirect(url_for('login.tela_login'))

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cliente WHERE email_cliente = %s AND senha_cliente = %s", (email, senha))
        cliente = cur.fetchone()
        cur.close()
        conn.close()

        if cliente:
            return redirect(url_for('cliente.encon_desp_serv'))
        else:
            flash("Email ou senha incorretos.", "erro")
            return redirect(url_for('login.tela_login'))  
        
    except Exception as e:
        flash(f"Ocorreu um erro: {str(e)}", "erro")
        return redirect(url_for('login.tela_login')) 

