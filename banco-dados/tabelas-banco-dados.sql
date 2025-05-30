CREATE TABLE Cliente (
    cpf_cliente VARCHAR(11) PRIMARY KEY NOT NULL,
    rg_cliente VARCHAR(20),
    nome_cliente VARCHAR(100) NOT NULL,
    nasc_cliente DATE,
    tele_pessoal_cliente VARCHAR(20),
    email_cliente VARCHAR(100) UNIQUE NOT NULL,
    senha_cliente VARCHAR(255) NOT NULL,
    status_conta BOOLEAN DEFAULT TRUE,
    ult_atualiz TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE Endereco (
    id_endereco SERIAL PRIMARY KEY,
    cpf_cliente VARCHAR(11) NOT NULL,
    tele_resid_cliente VARCHAR(20),
    endereco_cliente VARCHAR(100),
    num_cliente INTEGER,
    bairro_cliente VARCHAR(100),
    cep_cliente VARCHAR(8),
    cidade_cliente VARCHAR(50),
    estado_cliente VARCHAR(2),
    FOREIGN KEY (cpf_cliente) REFERENCES Cliente(cpf_cliente)
);

CREATE TABLE Despachante (
    cpf_desp VARCHAR(11) PRIMARY KEY NOT NULL,
    rg_desp VARCHAR(20) NOT NULL,
    nome_desp VARCHAR(100) NOT NULL,
    nasc_desp DATE NOT NULL,
    tele_pessoal_desp VARCHAR(20) NOT NULL,
    email_desp VARCHAR(100) NOT NULL UNIQUE,
    senha_desp VARCHAR(255) NOT NULL,
    regis_crdd VARCHAR(255) NOT NULL,
    data_exp_regis DATE NOT NULL,
    status_conta BOOLEAN DEFAULT TRUE,
    ult_atualiz TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE Estabelecimento (
    id_endereco SERIAL PRIMARY KEY,
    cpf_desp VARCHAR(11) NOT NULL,
    tele_comercial VARCHAR(20) NOT NULL,
    endereco_desp VARCHAR(100) NOT NULL,
    num_desp INTEGER NOT NULL,
    bairro_desp VARCHAR(100) NOT NULL,
    cep_desp VARCHAR(8) NOT NULL,
    cidade_desp VARCHAR(50) NOT NULL,
    estado_desp VARCHAR(2) NOT NULL,
    FOREIGN KEY (cpf_desp) REFERENCES Despachante(cpf_desp)
);

CREATE TABLE servico (
    id_servico SERIAL PRIMARY KEY,
    cpf_desp VARCHAR(14) NOT NULL,
    nome_servico VARCHAR(100) NOT NULL,
    descricao_servico TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ult_atualiz TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_despachante
        FOREIGN KEY (cpf_desp) REFERENCES despachante(cpf_desp)
        ON DELETE CASCADE
);

CREATE TABLE documento (
    id_documento SERIAL PRIMARY KEY,
    id_servico INT NOT NULL,
    nome_doc VARCHAR(100) NOT NULL,

    CONSTRAINT fk_servico
        FOREIGN KEY (id_servico) REFERENCES servico(id_servico)
        ON DELETE CASCADE
);

/*
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
*/