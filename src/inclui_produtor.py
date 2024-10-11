import cx_Oracle
import pandas as pd
import configparser
import os

#função para ler o arquivo de configuração
def ler_config(arquivo_config):
    config = configparser.ConfigParser()
    config.read(arquivo_config)
    return config

#função para carregar o CSV em um dicionário
def carregar_csv_para_dicionario(csv_file):
    df = pd.read_csv(csv_file, sep=';', encoding='utf-8')
    dados_dicionario = df.to_dict(orient='records')  #converter dataframe em uma lista de dicionários
    return dados_dicionario

#função para inserir os dados no banco de dados Oracle a partir do dicionário
def inserir_dados_oracle(dados, tabela, conn, output_dir):
    sql = f"""
    INSERT INTO {tabela} (
        cpf_cnpj, nome, endereco, telefone, email, consentimento, 
        nome_propriedade, area_total, area_plantada_milho, 
        area_plantada_soja, rua, numero, cidade, estado
    ) VALUES (
        :cpf_cnpj, :nome, :endereco, :telefone, :email, :consentimento, 
        :nome_propriedade, :area_total, :area_plantada_milho, 
        :area_plantada_soja, :rua, :numero, :cidade, :estado
    )
    """
    
    cursor = conn.cursor()
    erros_duplicados = []  #lista para armazenar os CPFs/CNPJs duplicados

    for registro in dados:
        try:
            cursor.execute(sql, registro)  #uso do dicionário diretamente para passar os parâmetros
        except cx_Oracle.IntegrityError as e:
            error_obj, = e.args
            # Verificar se é erro de chave duplicada (ORA-00001)
            if error_obj.code == 1:
                cpf_cnpj = registro['cpf_cnpj']
                erros_duplicados.append(cpf_cnpj)
                print(f"Erro de chave duplicada para CPF/CNPJ: {cpf_cnpj}")
    
    conn.commit()
    cursor.close()

    #se houver erros de duplicação, gerar um arquivo txt com os CPFs/CNPJs duplicados
    if erros_duplicados:
        erro_file = os.path.join(output_dir, 'erros_duplicados.txt')
        with open(erro_file, 'w') as f:
            for erro in erros_duplicados:
                f.write(f"CPF/CNPJ duplicado: {erro}\n")
        print(f"Arquivo de erros gerado: {erro_file}")

    print(f"Dados inseridos na tabela {tabela} com sucesso.")

#função principal
def main():
    #ler arquivo de configuração
    config = ler_config('../config/config.ini')

    #dados de conexão ao Oracle
    host = config['db']['host']
    user = config['db']['user']
    password = config['db']['password']
    sid = config['db']['SID']
    port = config['db'].getint('porta')

    #diretórios
    input_dir = config['dir']['input']
    output_dir = config['dir']['output']

    #arquivo CSV a ser importado
    csv_file = os.path.join(input_dir, 'pequenos_produtores.csv')

    #carregar o CSV em um dicionário
    dados = carregar_csv_para_dicionario(csv_file)
    print("Dados carregados no dicionário com sucesso.")
    
    #string de conexão Oracle
    dsn = cx_Oracle.makedsn(host, port, sid)
    
    #conectar ao banco de dados Oracle
    conn = cx_Oracle.connect(user=user, password=password, dsn=dsn)

    try:
        #inserir os dados no banco de dados a partir do dicionário
        inserir_dados_oracle(dados, 'produtores', conn, output_dir)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
