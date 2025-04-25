from database import Base, engine
from Utilidades.Funcoes import limpar_tela

from models.item import Item
from models.clientes import Cliente
from models.item_pedido import Item_Pedido
from models.pedidos import Pedido

Base.metadata.create_all(engine)  # Cria todas as tabelas definidas na classe base no banco de dados, se ainda não existirem

while True:  # menu interativo
    try:
        opcao = int(input("""Escolha uma opção:
        [ 1 ] Realizar orçamento
        [ 2 ] Alterar
        [ 3 ] Exibir
        [ 4 ] Deletar
        [ 5 ] Adicionar
        [ 6 ] Sair
        Digite aqui: """))
    except ValueError:
        limpar_tela()
        print("Oops! Parece que você digitou um caractere que não é um número, por favor tente de novo.")
        continue

    #Instânciando as tabelas
    item_instancia = Item()
    cliente_instancia = Cliente()
    itemPedido_instancia = Item_Pedido()
    pedido_instancia = Pedido()
    
    if opcao == 1:
        limpar_tela()
        pedido_instancia.Criar_pedido()
        
    elif opcao == 2:
        try:
            opcao = int(input("""Escolha uma opção:
            [ 1 ] Alterar Item
            [ 2 ] Alterar Cliente
            [ 3 ] Alterar Pedido
            Digite aqui: """))
        except ValueError:
            limpar_tela()
            print("Oops! Parece que você digitou um caractere que não é um número, por favor tente de novo.")
            continue

        if opcao == 1:
            item_instancia.Alterar_item()
        elif opcao == 2:
            cliente_instancia.Alterar_cliente()
        elif opcao == 3:
            pedido_instancia.Alterar_pedido()

    elif opcao == 3:
        try:
            opcao = int(input("""O que você deseja visualizar? 
                [ 1 ] Item
                [ 2 ] Cliente
                [ 3 ] Pedido  
                Digite aqui: """))
        except ValueError:
            limpar_tela()
            print("Ops! Parece que você digitou um caractere que não é número, tente novamente:")
            continue

        if opcao == 1:
            item_instancia.Exibir_item()

        elif opcao == 2:
            cliente_instancia.exibir_cliente()

        elif opcao == 3:
            pedido_instancia.Exibir_Pedido()

    elif opcao == 4:
        try:
            opcao = int(input("""Escolha uma opção:
            [ 1 ] Deletar Item
            [ 2 ] Deletar Cliente
            [ 3 ] Deletar Pedido
            Digite aqui: """))
        except ValueError:
            limpar_tela()
            print("Oops! Parece que você digitou um caractere que não é um número, por favor tente de novo.")
            continue

        if opcao == 1:
            item_instancia.Deletar_item()
        elif opcao == 2:
            cliente_instancia.Deletar_cliente()
        elif opcao == 3:
            pedido_instancia.deletar_pedido()

    elif opcao == 5:
        try:
            opcao = int(input("""Escolha uma opção:
            [ 1 ] Adicionar Item
            [ 2 ] Adicionar Cliente
            Digite aqui: """))
        except ValueError:
            limpar_tela()
            print("Oops! Parece que você digitou um caractere que não é um número, por favor tente de novo.")
            continue

        if opcao == 1:
            item_instancia.Adicionar_Item()
        elif opcao == 2:
            cliente_instancia.adicionar_cliente()

    elif opcao == 6:
        print("Finalizando execução")
        break