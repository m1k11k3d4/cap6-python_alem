import subprocess

def menu():
    while True:
        print("Escolha uma opção:")
        print("1 - Incluir Produtores")
        print("2 - Alterar o Produtor")
        print("3 - Excluir o Produtor")
        print("4 - Encontrar Produtores do Mesmo Estado para Compra de Insumos e Listar em JSON")
        print("5 - Calcular o Preço do Crédito de Carbono")
        print("6 - Sair")
        
        opcao = input("Digite o número da opção desejada: ")

        if opcao == "1":
            subprocess.run(['python', 'inclui_produtor.py'])
        elif opcao == "2":
            subprocess.run(['python', 'alterar_produtor.py'])
        elif opcao == "3":
            subprocess.run(['python', 'excluir_produtor.py'])
        elif opcao == "4":
            subprocess.run(['python', 'mostrar_produtores.py'])
        elif opcao == "5":
            subprocess.run(['python', 'gee.py'])
        elif opcao == "6":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
