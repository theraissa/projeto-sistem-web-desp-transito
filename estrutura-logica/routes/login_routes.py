from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from db import get_connection

login_bp = Blueprint('login', __name__)

@login_bp.route('/')
def tela_login():
    return render_template('login/login.html')

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

        # Verifica se é cliente
        cur.execute("SELECT cpf_cliente, nome_cliente FROM cliente WHERE email_cliente = %s AND senha_cliente = %s", (email, senha))
        cliente = cur.fetchone()

        if cliente:
            session['cliente_id'] = cliente[0]
            session['cliente_nome'] = cliente[1]
            cur.close()
            conn.close()
            return redirect(url_for('cliente.encon_desp_serv'))

        # Se não for cliente, verifica se é despachante
        cur.execute("SELECT cpf_desp, nome_desp FROM despachante WHERE email_desp = %s AND senha_desp = %s", (email, senha))
        despachante = cur.fetchone()

        cur.close()
        conn.close()

        if despachante:
            session['desp_id'] = despachante[0]
            session['desp_nome'] = despachante[1]
            return redirect(url_for('despachante.servico_desp'))

        # Se não encontrar nenhum
        flash("Email ou senha incorretos.", "erro")
        return redirect(url_for('login.tela_login'))

    except Exception as e:
        flash(f"Ocorreu um erro: {str(e)}", "erro")
        return redirect(url_for('login.tela_login')) 

@login_bp.route('/logout')
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "sucesso")
    return redirect(url_for('login.tela_login'))