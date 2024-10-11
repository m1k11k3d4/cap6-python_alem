CREATE TABLE produtores (    
    cpf_cnpj VARCHAR2(14),      		-- CPF (11 caracteres) ou CNPJ (14 caracteres)
	nome VARCHAR2(100),        		 	-- Nome completo, limite de 100 caracteres
    endereco VARCHAR2(255),     		-- Endereço completo, limite de 255 caracteres
    telefone VARCHAR2(15),      		-- Telefone com DDD, limite de 15 caracteres
    email VARCHAR2(100),        		-- E-mail, limite de 100 caracteres
    consentimento CHAR(1),       		-- Consentimento (S/N) para uso de dados
    nome_propriedade VARCHAR2(100),     -- Nome da propriedade (até 100 caracteres)
    area_total NUMBER(10, 2),           -- Área total da propriedade em hectares, com 2 casas decimais
    area_plantada_milho NUMBER(10, 2),  -- Área plantada de milho em hectares, com 2 casas decimais
    area_plantada_soja NUMBER(10, 2),   -- Área plantada de soja em hectares, com 2 casas decimais
    rua VARCHAR2(255) NOT NULL,         -- Localização completa (endereço ou coordenadas geográficas)
    numero VARCHAR2(20),
    cidade VARCHAR2(50) NOT NULL,       -- Cidade obrigatória
    estado VARCHAR2(3) NOT NULL,        -- Estado obrigatório
    CONSTRAINT pk_produtores PRIMARY KEY (cpf_cnpj)
);