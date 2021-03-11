'''
Classe com menus aprensentados para interface como usuário.
Pensar em um hierarquia para todas as funções
Opções de escolha para os relatórios
Opções de escolha para exportação de arquivos
Opções de escolha para atalzição dos dados
'''

#Exemplo

def menuOpcao():
    opcao = 0

    print("Digite a opção que deseja executar:\n"
          "1 - Vol +\n"
          "2 - Vol -\n"
          "3 - Canal \n"
          "4 - Home \n"
          "5 - Power on/off\n")

    while opcao < 1 or opcao > 5:
        opcao = int(input("Digite uma opção válida (1 - 5): "))
        if opcao < 1 or opcao > 5:
            print("Opção inválida. Digite novamente")

    return opcao

if __name__ == '__main__':
    opcao = menuOpcao()
    tv = televisao(20, 4)

    while opcao >= 1 and opcao <= 6:
        # AUMENTA VOLUME
        if opcao == 1:
            tv.aumenta_volume()
            print("---------------")
            print(f"Volume: {tv.volume}")
            print("---------------")


        # DIMINUI O VOLUME
        elif opcao == 2:
            tv.diminui_volume()
            print("---------------")
            print(f"Volume: {tv.volume}")
            print("---------------")

        # TROCA O CANAL
        elif opcao == 3:
            op = int(input("Escolha o canal desejado: "))
            tv.set_canal(op)
            print("---------------")
            print(f"Canal: {tv.canal}")
            print("---------------")

        # CONSULTA VOLUME E CANAL
        elif opcao == 4:
            print("--------HOME--------")
            print(f"O Volume está em: {tv.volume}")
            print(f"O canal está em: {tv.canal}")
            print("--------------------")

        # DESLIGAR A TV
        elif opcao == 5:
            print("-------------------")
            print("Aparelho desligado.")
            print("-------------------")
            opcao = 6

        if opcao != 6:
            opcao = menuOpcao()