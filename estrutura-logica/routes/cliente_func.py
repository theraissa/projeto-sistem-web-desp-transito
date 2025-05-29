from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_connection
from unidecode import unidecode

cliente_bp = Blueprint('cliente', __name__)

# Se o login ocorrer tudo certo, será encaminhado para essa tela
@cliente_bp.route('/encontrarServicos')
def encon_desp_serv():
    cliente_id = session.get('cliente_id')

    if not cliente_id:
        flash("Você precisa estar logado.", "erro")
        return redirect(url_for('login.tela_login'))

    #para obter os valores dos parâmetros da URL.
    pesquisar_cidade_original = request.args.get('cidade')
    pesquisar_desp_original = request.args.get('nome')

    pesquisar_cidade = unidecode(pesquisar_cidade_original).lower() if pesquisar_cidade_original else None
    pesquisar_desp = unidecode(pesquisar_desp_original).lower() if pesquisar_desp_original else None

    try:
        conn = get_connection()
        cur = conn.cursor()

        query = """
            SELECT d.*
            FROM despachante d
            INNER JOIN estabelecimento e ON d.cpf_desp = e.cpf_desp
            WHERE 1=1
        """
        params = []

        if pesquisar_desp:
            query += " AND LOWER(d.nome_desp) LIKE %s"
            params.append(f"%{pesquisar_desp}%")

        if pesquisar_cidade:
            query += " AND LOWER(e.cidade_desp) LIKE %s"
            params.append(f"%{pesquisar_cidade}%")

        cur.execute(query, params)
        despachantes = cur.fetchall()

        cur.close()
        conn.close()

        return render_template('telas-cliente/encon-desp-serv/encon-desp-serv.html', despachantes=despachantes)

    except Exception as e:
        flash(f"Ocorreu um erro: {str(e)}", "erro")
        return render_template('telas-cliente/encon-desp-serv/encon-desp-serv.html', despachantes=[])

@cliente_bp.route('/chamadoCliente')
def chamado_cliente():
    cliente_id = session.get('cliente_id')

    if not cliente_id:
        flash("Você precisa estar logado.", "erro")
        return redirect(url_for('login.tela_login'))

    return render_template('telas-cliente/chamado-cliente/chamado-cliente.html')

@cliente_bp.route('/perfilCliente', methods=['GET'])
def perfil_cliente():
    cliente_id = session.get('cliente_id')

    if not cliente_id:
        flash("Você precisa estar logado.", "erro")
        return redirect(url_for('login.tela_login'))

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Busca dados pessoais
        cur.execute("SELECT * FROM cliente WHERE cpf_cliente = %s", (cliente_id,))
        cliente = cur.fetchone()
        # Busca endereço
        cur.execute("SELECT * FROM endereco WHERE cpf_cliente = %s", (cliente_id,))
        endereco = cur.fetchone()

        cur.close()
        conn.close()

        return render_template('telas-cliente/perfil-cliente/perfil-cliente.html', cliente=cliente, endereco=endereco)

    except Exception as e:
        flash(f"Erro ao carregar perfil: {str(e)}", "erro")
        return redirect(url_for('cliente.inicial_cliente'))

@cliente_bp.route('/perfilCliente', methods=['POST'])
def atualizar_perfil_cliente():
    cliente_id = session.get('cliente_id')

    if not cliente_id:
        flash("Você precisa estar logado.", "erro")
        return redirect(url_for('login.tela_login'))    

    #Dados do Cliente
    nome_cliente = request.form.get('nome_cliente')
    cpf_cliente = request.form.get('cpf_cliente')
    rg_cliente = request.form.get('rg_cliente')
    nasc_cliente = request.form.get('nasc_cliente')
    tele_pessoal_cliente = request.form.get('tele_pessoal_cliente')
    email_cliente = request.form.get('email_cliente')
    senha_cliente = request.form.get('senha_cliente')
    senha_confir = request.form.get('senha_confir')
    
    # Dados da Residencia
    tele_residencial = request.form.get('tele_residencial')
    endereco_cliente = request.form.get('endereco_cliente')
    num_cliente = request.form.get('num_cliente')
    bairro_cliente = request.form.get('bairro_cliente')
    cep_cliente = request.form.get('cep_cliente')
    cidade_cliente = request.form.get('cidade_cliente')
    estado_cliente = request.form.get('estado_cliente')
    
    if not all([nome_cliente, cpf_cliente, rg_cliente, nasc_cliente, tele_pessoal_cliente, email_cliente, senha_cliente,
            tele_residencial, endereco_cliente, num_cliente, bairro_cliente, cep_cliente, cidade_cliente, estado_cliente]) or senha_cliente != senha_confir:
        flash("Por favor, preencha todos os campos obrigatórios.", "erro")
        return redirect(url_for('cliente.perfil_cliente')) 

    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Atualiza cliente
        cur.execute("""
            UPDATE cliente 
            SET rg_cliente = %s, nome_cliente = %s, nasc_cliente = %s, tele_pessoal_cliente = %s, 
            email_cliente = %s, senha_cliente = %s WHERE cpf_cliente = %s
        """, (rg_cliente, nome_cliente, nasc_cliente, tele_pessoal_cliente, email_cliente, senha_cliente, cliente_id))

        cur.execute("SELECT 1 FROM endereco WHERE cpf_cliente = %s", (cliente_id,))
        endereco_existe = cur.fetchone()

        if endereco_existe:
            # Atualiza endereço
            cur.execute("""
                UPDATE endereco 
                SET tele_resid_cliente = %s, endereco_cliente = %s, num_cliente = %s, bairro_cliente = %s, 
                cep_cliente = %s, cidade_cliente = %s, estado_cliente = %s WHERE cpf_cliente = %s
            """, (tele_residencial, endereco_cliente, num_cliente, bairro_cliente, cep_cliente, cidade_cliente, estado_cliente, cliente_id))
        else:
            # Insere novo endereço
            cur.execute("""
                INSERT INTO endereco (cpf_cliente, tele_resid_cliente, endereco_cliente, num_cliente, bairro_cliente, 
                                    cep_cliente, cidade_cliente, estado_cliente) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (cliente_id, tele_residencial, endereco_cliente, num_cliente, bairro_cliente, cep_cliente, cidade_cliente, estado_cliente))

        conn.commit()
        cur.close()
        conn.close()
        
        flash("Perfil atualizado com sucesso!", "sucesso")
        return redirect(url_for('cliente.perfil_cliente'))
    
    except Exception as e:
        flash(f"Erro ao atualizar o perfil: {str(e)}", "erro")
        return redirect(url_for('cliente.perfil_cliente')) 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    return render_template('telas-cliente/perfil-cliente/perfil-cliente.html')
