
<img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=30% height=30%>

# AgroCoop Project Document - 1TIAOR - FIAP


## Grupo 13

#### Miki Ikeda - RM559882



## Sumário

[1. Introdução](#c1)

[2. Visão Geral do Projeto](#c2)

[3. Desenvolvimento do Projeto](#c3)

[4. Conclusões e Trabalhos Futuros](#c4)

[5. Referências](#c5)


<br>

# <a name="c1"></a>1. Introdução

## 1.1. Escopo do Projeto

### 1.1.1. Contexto do Agronegócio

Este trabalho envolve o desenvolvimento de uma cooperativa digital focada no agronegócio, especialmente para plantações de milho e soja, visando apoiar pequenos produtores e agricultores familiares. A cooperativa facilita o compartilhamento de recursos, compra coletiva de insumos por produtores do mesmo estado e cálculo de créditos de carbono, otimizando as operações agrícolas de forma sustentável.

### 1.1.2. Descrição da Solução Desenvolvida

O projeto desenvolvido é uma Cooperativa Digital que oferece:

- Redução de custos: Através de compras coletivas de insumos e compartilhamento de equipamentos.
- Colaboração: Troca de conhecimento entre os produtores.
- Incentivos verdes: Acesso a créditos de carbono para compensar a emissão de GEE (Gases de Efeito Estufa).

# <a name="c2"></a>2. Visão Geral do Projeto

## 2.1. Objetivos do Projeto

O objetivo principal é desenvolver uma cooperativa digital que ofereça suporte a pequenos e médios produtores de milho e soja, permitindo-lhes otimizar suas operações através da colaboração, compartilhamento de dados por Produtores do mesmo Estado para compra coletiva de insumos e cálculo para compra de crédito de carbono.

## 2.2. Público-Alvo

O público-alvo são pequenos produtores e produtores familiares de milho e soja que buscam melhorar suas operações agrícolas, reduzir custos e acessar tecnologias inovadoras para aumentar a produtividade e sustentabilidade.

## 2.3. Metodologia

O desenvolvimento do projeto seguiu uma metodologia incremental, onde as funcionalidades foram implementadas em fases:

1. Conexão com banco de dados (Oracle).
2. Implementação das funcionalidades básicas: cadastro de produtores e plantações, compartilhamento de dados por produtores do mesmo Estado para compra coletiva de insumos (só para produtor que aceitou compartilhar dados).
3. Cálculo de créditos de carbono para a compensação de emissões de gases de efeito estufa.
4. Testes e ajustes das funcionalidades e do desempenho.

# <a name="c3"></a>3. Desenvolvimento do Projeto

## 3.1. Tecnologias Utilizadas

  ### Python
  O Python foi utilizado como a principal linguagem de programação para implementar as funcionalidades do sistema da cooperativa digital. Ele foi escolhido pela sua flexibilidade, facilidade de uso e vasto ecossistema de bibliotecas, especialmente para conexões com banco de dados Oracle e manipulação de arquivos. Os seguintes programas foram implementados:
  - Menu principal (menu_principal.py) implementa um menu interativo para executar diferentes funcionalidades do sistema. Ele apresenta um menu com 6 opções que chamam scripts individuais por meio de subprocessos.

      1 - Incluir Produtores: Chama o script inclui_produtor.py, que faz a inclusão de dados de produtores do arquivo pequenos_produtores.csv na tabela proutores no banco de dados Oracle.
      
      2 - Alterar o Produtor: Executa o script alterar_produtor.py, que permite modificar os dados de um produtor, como nome, endereço e outras informações, com base no CPF/CNPJ.
      
      3 - Excluir o Produtor: Usa o script excluir_produtor.py, que exibe as informações de um produtor e solicita confirmação antes de excluí-lo do banco de dados.
      
      4 - Encontrar Produtores do Mesmo Estado para Compra de Insumos e Listar em JSON: Chama o script mostrar_produtores.py, que lista os produtores do mesmo estado para facilitar a organização de compras coletivas e exporta todos os produtores em formato JSON.
      
      5 - Calcular o Preço do Crédito de Carbono: Executa o script gee.py, que calcula os créditos de carbono com base nas áreas plantadas de milho e soja.
      
      6 - Sair: Encerra o programa.
    
  
  ### Oracle Database
  O banco de dados Oracle foi utilizado para armazenar as informações dos produtores. Cada script Python utiliza uma conexão direta com o Oracle para realizar operações de CRUD (Create, Read, Update, Delete):
  
  - Conexão: A conexão com o banco de dados Oracle é configurada no arquivo config.ini, onde são armazenadas as credenciais e o endereço do banco de dados.
  - Produtores e Plantação: Os dados dos produtores e suas plantações de milho e soja são armazenados e manipulados via scripts Python, garantindo a consistência dos dados.
  - Consultas e Alterações: Scripts como o mostrar_produtores.py são responsáveis por realizar consultas no banco, como buscar todos os produtores de um determinado estado, filtrando apenas aqueles que deram consentimento para compartilhar suas informações​(mostrar_produtores).
  
  ### Subalgoritmos: Funções
  - Cadastro de Produtores: Funções que leem os dados de arquivos CSV e inserem no banco de dados Oracle​(inclui_produtor).
  - Alteração de Dados: Funções que validam e atualizam os dados dos produtores no banco de dados​(alterar_produtor).
  - Cálculo de Créditos de Carbono: Função que calcula o crédito de carbono com base nas áreas plantadas de milho e soja, levando em consideração as emissões de CO2 e o sequestro pelo plantio direto​(gee).
  
  ### Estruturas de Dados
  - Dicionários: Para facilitar a manipulação dos dados carregados de arquivos CSV, os dados dos produtores são convertidos em dicionários antes de serem inseridos no banco de dados​(inclui_produtor).
  - Listas: Durante a leitura e processamento dos dados, listas são utilizadas para armazenar coleções de produtores e insumos temporariamente, permitindo o processamento eficiente de múltiplos registros.
  
  ### Manipulação de Dados e Relatórios
  Os scripts geram relatórios e saídas em arquivos JSON e CSV:
   
  - CSV: Arquivos CSV são usados para armazenar dados de produtores, como CPF, nome, endereço e áreas plantadas. Esses dados são carregados pelo script inclui_produtor.py, que os converte em um formato dicionário para posterior inserção no banco de dados Oracle​(inclui_produtor). 
  - JSON: O script mostrar_produtores.py exporta os dados de nome, telefone e email dos produtores para um arquivo JSON, facilitando o contato entre os produtores.
  - Arquivos de erro: Em caso de duplicação de dados, um arquivo txt é gerado com os detalhes dos registros que não puderam ser inseridos​(inclui_produtor).


# <a name="c4"></a>4. Conclusões e Trabalhos Futuros

O projeto atingiu seus principais objetivos ao criar uma plataforma digital que facilita a colaboração entre pequenos produtores e oferece acesso a tecnologias que antes eram inacessíveis individualmente. Futuras melhorias podem incluir:

- Expansão da base de dados para incluir mais culturas agrícolas.
- Implementação de análises preditivas baseadas em dados coletados pelos sensores.
- Integração de uma plataforma de monitoramento climático em tempo real.

# <a name="c5"></a>5. Referências

CNN Brasil, Agricultura Familiar: https://www.cnnbrasil.com.br/economia/macroeconomia/agricultura-familiar-brasileira-ocupa-8a-posicao-entre-os-maiores-produtores-de-alimentos-do-mundo-mostra-anuario/
