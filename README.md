# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Cap 6 - Python e além

## Grupo 13

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/miki-ikeda-880a141b2/">Miki Ikeda</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- Lucas Gomes Moreira
### Coordenador(a)
- André Godoi Chiovato


## 📜 Descrição

O projeto se concentra no desenvolvimento de uma cooperativa digital voltada para o agronegócio, especificamente para apoiar pequenos produtores e agricultores familiares focados nas culturas de milho e soja. Segundo a <a href="https://www.cnnbrasil.com.br/economia/macroeconomia/agricultura-familiar-brasileira-ocupa-8a-posicao-entre-os-maiores-produtores-de-alimentos-do-mundo-mostra-anuario/">CNN Brasil</a> , o Brasil abriga 3,9 milhões de propriedades agrícolas, representando 77% dos estabelecimentos rurais, com 10,1 milhões de trabalhadores. Este projeto busca oferecer a esses produtores um espaço colaborativo para compartilhamento de recursos, compra coletiva de insumos por produtores do mesmo estado e cálculo de créditos de carbono, otimizando as operações agrícolas de forma sustentável


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>config</b>: Arquivo config.ini para incluir os dados de banco de dados e ajustar o diretório de input e de output (mais detalhes no readme.md nessa pasta).

- <b>data</b>: O arquivo pequenos_produtores.csv contém dados fictícios sobre os produtores, considerando que se trata de uma cooperativa, por isso inclui várias informações de diversos produtores. Este arquivo é utilizado para inserir esses dados no banco de dados. Já o arquivo ddl.sql contém o script de criação da tabela produtores, essencial para o funcionamento do sistema.

- <b>document</b>: explicação mais aprofundada do projeto.

- <b>src</b>: todos os programas pythons.

#### Não mova os scripts nem o arquivo de configuração config.ini das pastas originais, pois isso pode comprometer o funcionamento do programa. Ele está configurado para ser executado a partir dessas pastas.

## 🔧 Como executar o código

1. Pré-requisitos
Certifique-se de que você tenha as seguintes ferramentas instaladas:

- Python 3.x (preferencialmente 3.9 ou superior)
- Oracle Database ou acesso a uma instância do Oracle (para armazenar os dados)
- Bibliotecas Python: Você precisará instalar as bibliotecas listadas no arquivo requirements.txt

2. Instalar Dependências
No diretório principal do projeto src, execute o seguinte comando para instalar as dependências necessárias:

  ```python
   pip install -r requirements.txt
 ```
  Isso instalará as bibliotecas como cx_Oracle, pandas, e configparser.

3. Executar o conteúdo do ddl.sql no banco de dados que será utilizado, para criar a tabela PRODUTORES.

4. Configurar o arquivo config.ini.

5. Executar o Menu Principal
O projeto é executado a partir do menu principal, que oferece várias opções de funcionalidades como incluir, alterar, excluir produtores, calcular créditos de carbono, etc.
Execute o script menu_principal.py.
 
  ```python
  python menu_principal.py
 ```

## 🗃 Histórico de lançamentos

* 0.1.0 - 09/10/2024
    *

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


