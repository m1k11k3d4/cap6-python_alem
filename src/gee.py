import cx_Oracle
import configparser

#função para ler o arquivo de configuração
def ler_config(arquivo_config):
    config = configparser.ConfigParser()
    config.read(arquivo_config)
    return config

#função para calcular o crédito de carbono e o valor em R$
def calcular_credito_carbono(area_milho, area_soja, preco_por_tonelada=60):
    #emissões médias (toneladas CO2/ha/ano)
    emissoes_milho = 2.8  # Emissões por hectare para milho
    emissoes_soja = 2.2   # Emissões por hectare para soja
    
    #sequestro pelo plantio direto (toneladas CO2/ha/ano)
    sequestro_milho = 0.8  # Sequestro por hectare para milho
    sequestro_soja = 0.7   # Sequestro por hectare para soja

    #calculo do crédito de carbono por hectare
    credito_milho = (emissoes_milho - sequestro_milho) * area_milho
    credito_soja = (emissoes_soja - sequestro_soja) * area_soja

    #total de créditos de carbono
    total_credito = credito_milho + credito_soja
    
    #valor em reais
    valor_total = total_credito * preco_por_tonelada
    return total_credito, credito_milho, credito_soja, valor_total

#função para obter as áreas plantadas de milho e soja pelo CPF/CNPJ
def obter_areas(conn, cpf_cnpj):
    sql = """
    SELECT AREA_PLANTADA_MILHO, AREA_PLANTADA_SOJA 
    FROM produtores 
    WHERE cpf_cnpj = :cpf_cnpj
    """
    cursor = conn.cursor()
    cursor.execute(sql, {'cpf_cnpj': cpf_cnpj})
    resultado = cursor.fetchone()
    
    cursor.close()
    return resultado

#função para solicitar o CPF/CNPJ e validar se está no banco
def solicitar_cpf_cnpj(conn):
    while True:
        cpf_cnpj = input("Informe o CPF/CNPJ do produtor (somente números): ")
        areas = obter_areas(conn, cpf_cnpj)
        if areas:
            return cpf_cnpj, areas
        else:
            print("CPF/CNPJ não encontrado. Tente novamente.")

#função principal para conectar ao banco e calcular os créditos de carbono
def main():
    #ler as configurações do arquivo config.ini
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
        #solicitar e validar o CPF/CNPJ
        cpf_cnpj, areas = solicitar_cpf_cnpj(conn)
        area_milho, area_soja = areas

        #calcular os créditos de carbono e o valor total
        total_credito, credito_milho, credito_soja, valor_total = calcular_credito_carbono(area_milho, area_soja)
        
        #exibir os resultados com as áreas plantadas
        print(f"Áreas plantadas: Milho: {area_milho:.2f} ha, Soja: {area_soja:.2f} ha")
        print(f"Crédito de carbono total: {total_credito:.2f} toneladas de CO2")
        print(f"Crédito de carbono para milho: {credito_milho:.2f} toneladas de CO2")
        print(f"Crédito de carbono para soja: {credito_soja:.2f} toneladas de CO2")
        print(f"Valor total em reais: R$ {valor_total:.2f}")

    finally:
        conn.close()

if __name__ == "__main__":
    main()
