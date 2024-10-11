import cx_Oracle
import configparser

#função para ler o arquivo de configuração
def ler_config(arquivo_config):
    config = configparser.ConfigParser()
    config.read(arquivo_config)
    return config

#função para buscar o produtor pelo CPF/CNPJ
def buscar_produtor_por_cpf(conn, cpf_cnpj_informado):
    sql = """
    SELECT cpf_cnpj, nome, telefone, email, estado 
    FROM produtores 
    WHERE cpf_cnpj = :cpf_cnpj
    """
    cursor = conn.cursor()
    cursor.execute(sql, {'cpf_cnpj': cpf_cnpj_informado})
    produtor_info = cursor.fetchone()
    cursor.close()
    
    return produtor_info

#função para excluir o produtor pelo CPF/CNPJ
def excluir_produtor(conn, cpf_cnpj_informado):
    sql = """
    DELETE FROM produtores 
    WHERE cpf_cnpj = :cpf_cnpj
    """
    cursor = conn.cursor()
    cursor.execute(sql, {'cpf_cnpj': cpf_cnpj_informado})
    conn.commit()
    cursor.close()
    print(f"Produtor com CPF/CNPJ {cpf_cnpj_informado} foi excluído com sucesso.")

#função para solicitar o CPF/CNPJ e validar se está no banco
def solicitar_cpf_cnpj(conn):
    while True:
        cpf_cnpj_informado = input("Informe o CPF/CNPJ do produtor (somente números): ")
        
        #buscar o produtor no banco
        produtor_info = buscar_produtor_por_cpf(conn, cpf_cnpj_informado)
        
        if produtor_info:
            #exibir as informações do produtor antes de excluir
            print(f"CPF/CNPJ: {produtor_info[0]}")
            print(f"Nome: {produtor_info[1]}")
            print(f"Telefone: {produtor_info[2]}")
            print(f"Email: {produtor_info[3]}")
            print(f"Estado: {produtor_info[4]}")
            
            #solicitar confirmação para excluir
            confirmacao = input("Tem certeza que deseja excluir este produtor? (S/N): ").upper()
            if confirmacao == 'S':
                excluir_produtor(conn, cpf_cnpj_informado)
            else:
                print("Exclusão cancelada.")
            return
        else:
            print(f"CPF/CNPJ {cpf_cnpj_informado} não encontrado. Tente novamente.")

#função principal para conectar ao banco de dados e executar o programa
def main():
    # Ler as configurações do arquivo config.ini
    config = ler_config('../config/config.ini')

    #obter as credenciais e parâmetros de conexão
    host = config['db']['host']
    porta = config['db']['porta']
    SID = config['db']['SID']
    user = config['db']['user']
    password = config['db']['password']

    #conectar ao banco de dados Oracle
    dsn = cx_Oracle.makedsn(host, porta, SID)
    conn = cx_Oracle.connect(user=user, password=password, dsn=dsn)

    try:
        #solicitar o CPF/CNPJ e excluir o produtor
        solicitar_cpf_cnpj(conn)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
