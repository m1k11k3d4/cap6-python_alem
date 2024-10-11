import cx_Oracle
import configparser
import json
import os

#função para ler o arquivo de configuração
def ler_config(arquivo_config):
    config = configparser.ConfigParser()
    config.read(arquivo_config)
    return config

#função para buscar produtores pelo CPF/CNPJ e estado, exibindo consentidos e exportando para JSON
def buscar_produtores_por_estado(conn, cpf_cnpj_informado, output_dir):
    #verificar se o CPF/CNPJ informado está na base de dados
    sql_produtor = """
    SELECT estado, nome, telefone, email, consentimento 
    FROM produtores 
    WHERE cpf_cnpj = :cpf_cnpj
    """
    cursor = conn.cursor()
    cursor.execute(sql_produtor, {'cpf_cnpj': cpf_cnpj_informado})
    produtor_info = cursor.fetchone()

    if not produtor_info:
        return False, None

    estado, nome, telefone, email, consentimento = produtor_info

    #buscar outros produtores no mesmo estado que deram consentimento 'S' e não são o próprio produtor informado
    sql_outros_produtores = """
    SELECT nome, telefone, email 
    FROM produtores 
    WHERE estado = :estado AND consentimento = 'S' AND cpf_cnpj != :cpf_cnpj
    """
    cursor.execute(sql_outros_produtores, {'estado': estado, 'cpf_cnpj': cpf_cnpj_informado})
    produtores_mesmo_estado = cursor.fetchall()

    if not produtores_mesmo_estado:
        print(f"Não há outros produtores no estado {estado} que deram consentimento.")
        return True, None

    #lista para exportação de JSON
    produtores_list = []

    #exibir os dados dos produtores com consentimento (exceto o próprio) e adicionar à lista para JSON
    for nome, telefone, email in produtores_mesmo_estado:
        print(f"Nome: {nome}")
        print(f"Telefone: {telefone}")
        print(f"Email: {email}")
        print("-" * 40)

        produtores_list.append({
            'nome': nome,
            'telefone': telefone,
            'email': email
        })

    #criar dicionário final para exportar em JSON
    json_resultado = {
        'estado': estado,
        'produtores': produtores_list
    }

    #garantir que o diretório de output existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    #caminho completo para o arquivo JSON
    json_file_path = os.path.join(output_dir, 'produtores_resultado.json')

    #exportar para um arquivo JSON no diretório de output
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_resultado, json_file, ensure_ascii=False, indent=4)

    print(f"\nResultado exportado para '{json_file_path}'.")

    return True, estado

#função para solicitar o CPF/CNPJ e garantir que seja válido
def solicitar_cpf_cnpj(conn, output_dir):
    while True:
        cpf_cnpj_informado = input("Informe o CPF/CNPJ do produtor (somente números): ")
        valido, estado = buscar_produtores_por_estado(conn, cpf_cnpj_informado, output_dir)
        
        if valido:
            return
        else:
            print(f"CPF/CNPJ {cpf_cnpj_informado} não encontrado. Tente novamente.")

#função principal para conectar ao banco de dados e executar o programa
def main():
    #ler as configurações do arquivo config.ini
    config = ler_config('../config/config.ini')

    #obter as credenciais e parâmetros de conexão
    host = config['db']['host']
    porta = config['db']['porta']
    SID = config['db']['SID']
    user = config['db']['user']
    password = config['db']['password']

    #obter o diretório de output do arquivo de configuração
    output_dir = config['dir']['output']

    #conectar ao banco de dados Oracle
    dsn = cx_Oracle.makedsn(host, porta, SID)
    conn = cx_Oracle.connect(user=user, password=password, dsn=dsn)

    try:
        #solicitar o CPF/CNPJ e buscar os dados do produtor e de outros consentidos no mesmo estado
        solicitar_cpf_cnpj(conn, output_dir)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
