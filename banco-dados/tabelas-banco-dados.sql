CREATE TABLE Cadastro_Cliente (
    cpf_cliente VARCHAR(14) PRIMARY KEY,
    rg_cliente INT,
    nome_cliente VARCHAR(100),
    nasc_cliente DATE,
    tele_pessoal_cliente VARCHAR(15),
    telefone_residencial_cliente VARCHAR(15),
    email_cliente VARCHAR(100),
    endereco_cliente VARCHAR(255),
    bairro_cliente VARCHAR(100),
    n_casa_cliente INT,
    cep_cliente VARCHAR(10),
    cidade_cliente VARCHAR(100),
    estado_cliente VARCHAR(50),
    status_conta BOOLEAN,
    ult_atualiz_cliente TIMESTAMP,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Perfil_Cliente (
    id_perfil_cliente SERIAL PRIMARY KEY,
    cpf_cliente VARCHAR(14) REFERENCES Cadastro_Cliente(cpf_cliente),
    campo_alterado_cliente VARCHAR(100),
    valor_novo_cliente VARCHAR(255),
    status_perfil_cliente VARCHAR(50),
    data_solic_alter_cliente TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Cadastro_Despachante (
    cpf_desp VARCHAR(14) PRIMARY KEY,
    rg_desp INT,
    nome_desp VARCHAR(100),
    nasc_desp DATE,
    tele_pessoal_desp VARCHAR(15),
    tele_comercial_desp VARCHAR(15),
    email_desp VARCHAR(100),
    regis_crdd INT,
    data_expi_regis DATE,
    endereco_desp VARCHAR(255),
    bairro_desp VARCHAR(100),
    n_cada_desp INT,
    cep_desp VARCHAR(10),
    cidade_desp VARCHAR(100),
    estado_desp VARCHAR(50),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ult_atualiz_desp TIMESTAMP,
    status_conta BOOLEAN
);

CREATE TABLE Perfil_Despachante (
    id_perfil_desp SERIAL PRIMARY KEY,
    cpf_desp VARCHAR(14) REFERENCES Cadastro_Despachante(cpf_desp),
    campo_alterado_desp VARCHAR(100),
    valor_novo_desp VARCHAR(255),
    status_perfil_desp VARCHAR(50),
    data_solic_alter_desp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Servico (
    id_servico SERIAL PRIMARY KEY,
    cpf_desp VARCHAR(14) REFERENCES Cadastro_Despachante(cpf_desp),
    tipo_servico VARCHAR(100)
);

CREATE TABLE Chamado (
    id_chamado SERIAL PRIMARY KEY,
    cpf_cliente VARCHAR(14) REFERENCES Cadastro_Cliente(cpf_cliente),
    cpf_desp VARCHAR(14) REFERENCES Cadastro_Despachante(cpf_desp),
    id_servico INT REFERENCES Servico(id_servico),
    data_abertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_encerrado TIMESTAMP,
    status_chamado VARCHAR(50)
);

CREATE TABLE Agenda (
    id_agenda SERIAL PRIMARY KEY,
    id_chamado INT REFERENCES Chamado(id_chamado),
    cpf_desp VARCHAR(14) REFERENCES Cadastro_Despachante(cpf_desp),
    data_agendamento TIMESTAMP,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ult_atualiz_agenda TIMESTAMP,
    status_agenda VARCHAR(50)
);
