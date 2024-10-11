import cx_Oracle
import configparser
import re
import sys

#função para ler o arquivo de configuração
def ler_config(arquivo_config):
    config = configparser.ConfigParser()
    config.read(arquivo_config)
    return config

#depara entre labels e campos da tabela, com tipos de dados esperados
depara_labels = {
    1: ('Nome', 'nome', str),
    2: ('Endereço', 'endereco', str),
    3: ('Telefone', 'telefone', str),
    4: ('Email', 'email', str),
    5: ('Consentimento', 'consentimento', str),  # Deve ser 'S' ou 'N'
    6: ('Nome da Propriedade', 'nome_propriedade', str),
    7: ('Área Total', 'area_total', float),
    8: ('Área Plantada Milho', 'area_plantada_milho', float),
    9: ('Área Plantada Soja', 'area_plantada_soja', float),
    10: ('Rua', 'rua', str),
    11: ('Número', 'numero', str),
    12: ('Cidade', 'cidade', str),
    13: ('Estado', 'estado', str),  # Deve ter 2 letras
    0: ('Sair', None, None)  # Opção para sair do programa
}

#função para validar o valor inputado de acordo com o tipo esperado
def validar_valor(campo, valor):
    if campo == 'cpf_cnpj':
        if not re.match(r'^\d{11}|\d{14}$', valor):
            raise ValueError("CPF/CNPJ inválido. Deve ter 11 (CPF) ou 14 (CNPJ) dígitos numéricos.")
    elif campo == 'telefone':
        if not re.match(r'^\(\d{2}\)\s9?\d{4}-\d{4}$', valor):
            raise ValueError("Telefone inválido. Formato esperado: (XX) 99999-9999.")
    elif campo == 'email':
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', valor):
            raise ValueError("E-mail inválido.")
    elif campo == 'consentimento':
        if valor.upper() not in ['S', 'N']:
            raise ValueError("O consentimento deve ser 'S' ou 'N'.")
    elif campo == 'estado':
        if not re.match(r'^[A-Z]{2}$', valor):
            raise ValueError("Estado inválido. Deve ser composto por 2 letras maiúsculas(UF).")
    elif isinstance(valor, float):
        try:
            float(valor)
        except ValueError:
            raise ValueError(f"Valor inválido para {campo}. Deve ser numérico.")
    elif campo in ['area_total', 'area_plantada_milho', 'area_plantada_soja']:
        #verificar se é um número com ponto como separador decimal
        if not re.match(r'^\d+(\.\d+)?$', valor):
            raise ValueError(f"Valor inválido para {campo}. Utilize apenas números e ponto (.) para decimais.")

#função para obter o valor atual de um campo
def obter_valor_atual(conn, cpf_cnpj, campo):
    sql = f"SELECT {campo} FROM produtores WHERE cpf_cnpj = :cpf_cnpj"
    cursor = conn.cursor()
    cursor.execute(sql, {'cpf_cnpj': cpf_cnpj})
    resultado = cursor.fetchone()
    cursor.close()
    
    if resultado:
        return resultado[0]
    else:
        return None

#função para realizar a alteração no banco de dados
def alterar_dado(conn, cpf_cnpj, campo, valor_novo):
    sql = f"UPDATE produtores SET {campo} = :valor_novo WHERE cpf_cnpj = :cpf_cnpj"
    cursor = conn.cursor()
    cursor.execute(sql, {'valor_novo': valor_novo, 'cpf_cnpj': cpf_cnpj})
    conn.commit()
    cursor.close()
    print(f"O campo '{campo}' foi atualizado com sucesso para o CPF/CNPJ: {cpf_cnpj}.")

#função para obter input com validação
def obter_input_valido(prompt, campo_tabela):
    while True:
        valor = input(prompt)
        try:
            validar_valor(campo_tabela, valor)
            return valor
        except ValueError as ve:
            print(f"Erro: {ve}. Tente novamente.")

#função para alterar um campo
def alterar_campo(conn):
    cpf_cnpj = obter_input_valido("Informe o CPF/CNPJ do produtor: ", 'cpf_cnpj')

    while True:
        #exibir opções de campos para alteração com menu numerado e alinhado
        print("\nOpções de campos para alteração:")
        for num, (label, _, _) in depara_labels.items():
            print(f"{num:<2}. {label:<20}")  #alinhamento com 2 dígitos para o número e 20 caracteres para o label

        #solicitar a escolha do campo pelo número
        while True:
            try:
                opcao_campo = int(input("\nInforme o número do campo a ser alterado (ou 0 para sair): "))
                if opcao_campo not in depara_labels:
                    raise ValueError("Opção inválida. Escolha um número da lista.")
                break
            except ValueError as ve:
                print(f"Erro: {ve}. Tente novamente.")

        #se o usuário escolheu 'Sair', encerrar o programa
        if opcao_campo == 0:
            print("Saindo do programa.")
            sys.exit()  #encerra o programa completamente

        #obter o campo selecionado e seus detalhes
        label_campo, campo_tabela, tipo_campo = depara_labels[opcao_campo]

        #obter o valor atual do campo
        valor_atual = obter_valor_atual(conn, cpf_cnpj, campo_tabela)
        
        if valor_atual is None:
            print(f"CPF/CNPJ {cpf_cnpj} não encontrado.")
            return

        print(f"\nValor atual de {label_campo}: {valor_atual}")

        #solicitar o novo valor
        valor_novo = obter_input_valido(f"Informe o novo valor para {label_campo}: ", campo_tabela)

        #confirmar a alteração
        confirmar = input(f"\nConfirma a alteração de {label_campo} de '{valor_atual}' para '{valor_novo}'? (S/N): ").upper()

        if confirmar == 'S':
            #realizar a alteração no banco de dados
            alterar_dado(conn, cpf_cnpj, campo_tabela, valor_novo)
        else:
            print("Alteração cancelada.")

#função principal
def main():
    # Ler arquivo de configuração
    config = ler_config('../config/config.ini')

    #dados de conexão ao Oracle
    host = config['db']['host']
    user = config['db']['user']
    password = config['db']['password']
    sid = config['db']['SID']
    port = config['db'].getint('porta')

    #string de conexão Oracle
    dsn = cx_Oracle.makedsn(host, port, sid)

    #conectar ao banco de dados Oracle
    conn = cx_Oracle.connect(user=user, password=password, dsn=dsn)

    try:
        while True:
            alterar_campo(conn)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
