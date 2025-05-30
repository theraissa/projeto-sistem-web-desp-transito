from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_connection

desp_bp = Blueprint('despachante', __name__)

# Se o login ocorrer tudo certo, será encaminhado para essa tela
@desp_bp.route('/servicos')
def servico_desp():
    desp_id = session.get('desp_id')

    if not desp_id:
        flash("Você precisa estar logado.", "erro")
        return redirect(url_for('login.tela_login'))   
    
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id_servico, nome_servico 
            FROM servico 
            WHERE cpf_desp = %s
        """, (desp_id,))
        servicos = cur.fetchall()  # Lista de tuplas: [(id1, nome1), (id2, nome2), ...]

        cur.close()
        conn.close()

        return render_template('telas-despachantes/servico-desp/servico-desp.html', servicos=servicos)

    except Exception as e:
        flash(f"Erro ao carregar serviços: {str(e)}", "erro")
        return render_template('telas-despachantes/servico-desp/servico-desp.html', servicos=[])

@desp_bp.route('/criarNovoServico', methods=['GET', 'POST'])
def criar_servico():
    desp_id = session.get('desp_id')

    if not desp_id:
        flash("Você precisa estar logado.", "erro")
        return redirect(url_for('login.tela_login'))

    nome_servico = request.form.get('nome_servico')
    documentos = request.form.getlist('documento[]')
    
    #verificando se não há campos vazios
    if not nome_servico:
        flash("O nome do serviço é obrigatório.", "erro")
        return render_template('telas-despachantes/servico-desp/criar-serv/criar-serv.html')
    
    if not documentos:
        flash("É necessário pelo menos um documento.", "erro")
        return render_template('telas-despachantes/servico-desp/criar-serv/criar-serv.html')
    
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Insere o serviço e pega o ID gerado
        cur.execute("""
            INSERT INTO servico (cpf_desp, nome_servico)
            VALUES (%s, %s) RETURNING id_servico
        """, (desp_id, nome_servico))
        id_servico = cur.fetchone()[0]

        # Insere os documentos
        for doc in documentos:
            cur.execute("""
                INSERT INTO documento (id_servico, nome_doc)
                VALUES (%s, %s)
            """, (id_servico, doc))

        conn.commit()
        cur.close()
        conn.close()

        flash("Serviço e documentos criados com sucesso!", "sucesso")
        return redirect(url_for('despachante.servico_desp'))

    except Exception as e:
        flash(f"Erro ao criar serviço: {str(e)}", "erro")
        return render_template('telas-despachantes/servico-desp/criar-serv/criar-serv.html')

@desp_bp.route('/deletarServico', methods=['POST'])
def deletar_servico(id_servico):
    desp_id = session.get('desp_id')

    if not desp_id:
        flash("Você precisa estar logado.", "erro")
        return redirect(url_for('login.tela_login'))

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Confirma se o serviço pertence ao despachante logado
        cur.execute("""
            SELECT id_servico FROM servico WHERE id_servico = %s AND cpf_desp = %s
        """, (id_servico, desp_id))
        servico = cur.fetchone()

        if not servico:
            flash("Serviço não encontrado ou você não tem permissão.", "erro")
            return redirect(url_for('despachante.servico_desp'))

        # Deleta documentos relacionados
        cur.execute("""
            DELETE FROM documento WHERE id_servico = %s
        """, (id_servico,))

        # Deleta o serviço
        cur.execute("""
            DELETE FROM servico WHERE id_servico = %s
        """, (id_servico,))

        conn.commit()
        cur.close()
        conn.close()

        flash("Serviço excluído com sucesso.", "sucesso")
    except Exception as e:
        flash(f"Erro ao excluir serviço: {str(e)}", "erro")

    return redirect(url_for('despachante.servico_desp'))

@desp_bp.route('/chamados')
def chamado_desp():
    desp_id = session.get('desp_id')

    if not desp_id:
        flash("Você precisa estar logado.", "erro")
        return redirect(url_for('login.tela_login')) 
       
    return render_template('telas-despachantes/chamado-desp/chamado-desp.html')

@desp_bp.route('/agendamentos')
def agenda_desp():
    desp_id = session.get('desp_id')

    if not desp_id:
        flash("Você precisa estar logado.", "erro")
        return redirect(url_for('login.tela_login'))   
     
    return render_template('telas-despachantes/agend-desp/agend-desp.html')

@desp_bp.route('/perfil', methods=['GET'])
def perfil_desp():
    desp_id = session.get('desp_id')

    if not desp_id:
        flash("Você precisa estar logado.", "erro")
        return redirect(url_for('login.tela_login'))

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Busca dados pessoais
        cur.execute("SELECT * FROM despachante WHERE cpf_desp = %s", (desp_id,))
        despachante = cur.fetchone()
        # Busca endereço
        cur.execute("SELECT * FROM estabelecimento WHERE cpf_desp = %s", (desp_id,))
        estabelecimento = cur.fetchone()

        cur.close()
        conn.close()

        return render_template('telas-despachantes/perfil-desp/perfil-desp.html', despachante=despachante, estabelecimento=estabelecimento)

    except Exception as e:
        flash(f"Erro ao carregar perfil: {str(e)}", "erro")
        return redirect(url_for('despachante.servico_desp'))

@desp_bp.route('/perfil', methods=['POST'])
def atualizar_perfil_desp():
    desp_id = session.get('desp_id')

    if not desp_id:
        flash("Você precisa estar logado.", "erro")
        return redirect(url_for('login.tela_login'))    

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
        
        # Atualiza despachante
        cur.execute("""
            UPDATE despachante 
            SET rg_desp = %s, nome_desp = %s, nasc_desp = %s, tele_pessoal_desp = %s, 
            email_desp = %s, senha_desp = %s, regis_crdd = %s, data_exp_regis = %s WHERE cpf_desp= %s
        """, (rg_desp, nome_desp, nasc_desp, tele_pessoal_desp, email_desp, senha_desp, regis_crdd, data_exp_regis, desp_id))
        
        # Atualiza estabelecimento
        cur.execute("""
            UPDATE despachante 
            SET tele_comercial = %s, endereco_desp = %s, num_desp = %s, bairro_desp = %s, 
            cep_desp = %s, cidade_desp = %s, estado_desp = %s WHERE cpf_desp= %s
        """, (tele_comercial, endereco_desp, num_desp, bairro_desp, cep_desp, cidade_desp, estado_desp, desp_id))
        
        conn.commit()
        cur.close()
        conn.close()
        
        flash("Perfil atualizado com sucesso!", "sucesso")
        return redirect(url_for('cad_desp.perfil_desp'))
    
    except Exception as e:
        flash(f"Erro ao atualizar o perfil: {str(e)}", "erro")
        return redirect(url_for('cad_desp.perfil_desp')) 
    