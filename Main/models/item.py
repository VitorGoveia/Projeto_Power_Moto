from database import ModeloBase, session
from sqlalchemy import Column, String, Numeric
from Utilidades.Funcoes import limpar_tela

#Tabela de item:
class Item(ModeloBase):
    __tablename__ = 'itens'

    SKU = Column(String, primary_key=True)
    Valor_Unitario = Column(Numeric(10, 2))
    Nome_do_Item = Column(String)
    Marca = Column(String)

    def adicionar_Item(self):
        """Realiza a criação do item, valida se tem algum dado faltando"""

        sku_item = input('Digite a SKU do item: ')
        nome = input('Digite o nome do item: ').capitalize()

        while True:
            #Resgata o valor em formato de texto, dessa forma o usuário poderá digitar o valor com uma vírgula
            valor = input('Agora digite o valor unitário do item (com .):').replace(",",".")
            float(valor) #converte o valor de STR para FLOAT
            if valor != 0:
                break
            else:
                print("Valor do item não pode ser 0")

        marca_item = input('Digite a marca do item: ').capitalize()

        #.capitalize() para deixar apenas a primeira letra da frase em maiúsculo

        if not (sku_item or nome or valor or marca_item):
            print("Algum valor está em branco, operação cancelada")
        else:
            criar_item = session.query(Item).filter_by(SKU=sku_item).first()
            if criar_item: # Valida se já tem um item com a SKU digitada
                print("Já há um item com essa SKU!")
            else:
                criar_item = Item(SKU=sku_item,
                                  Nome_do_Item=nome,
                                  Valor_Unitario=valor,
                                  Marca=marca_item)
                session.add(criar_item)
                session.commit()
                print("Item adicionado com sucesso")
                print()

    def _exibir_detalhes_itens(self, item):
        """Função de exibir os detalhes (privada)"""

        print(f'{item.Nome_do_Item} ({item.SKU})')
        print(f'Valor: R${str(item.Valor_Unitario).replace(".",",")}')
        print(f'Marca: {item.Marca}')
        print()

    def exibir_item(self):
        limpar_tela()
        buscar = input("Digite a SKU do item ou deixe em branco para todos: ")
        if buscar:
            while True:
                item = session.query(Item).filter_by(SKU=buscar).first()
                if item:
                    self._exibir_detalhes_itens(item)
                    break
                else:
                    buscar = input("Item não existe! Digite novamente: ")
                    if not buscar:
                        break
        else:
            itens = session.query(Item).all()
            if not itens:
                print("Não há itens cadastrados")
            else:
                print('Esses são todos os itens em nosso Banco de Dados:\n')
                for item in itens:  # percorre o conjunto de matérias
                    self._exibir_detalhes_itens(item)

    def alterar_item(self):
        buscar = input("Digite a SKU do item que será alterado: ")
        while True:
            item = session.query(Item).filter_by(SKU=buscar).one_or_none()
            if not item:
                print("Erro: Nenhum item encontrado com essa SKU!")
            else:
                self._exibir_detalhes_itens(item)
            if item:
                while True:
                    try:
                        opcao = int(input("""O que você quer alterar?
                        [ 1 ] Nome
                        [ 2 ] Valor
                        [ 3 ] Marca_item
                        """))
                    except ValueError:
                        print("O valor não é válido! Digite novamente: ")
                        continue
                    if opcao == 1:
                        item.Nome_do_Item = input("Digite o novo nome do item: ")
                    elif opcao == 2:
                        item.Valor_Unitario = input("Digite o novo valor do item (com .): ")
                    elif opcao == 3:
                        item.Marca = input("Digite a nova marca do item: ")

                    session.commit()
                    print()
                    limpar_tela()
                    print("Alteração feita com sucesso!")
                    print()
                    break

                break
            else:
                buscar = input("Item não existe! Digite novamente: ")
                if not buscar:
                    break

    def deletar_item(self):
        from models.item_pedido import ItemPedido
        del_sku = input("Digite a SKU do item a ser deletado: ")
        del_item = session.query(Item).filter_by(SKU = del_sku).first()
        del_itens_pedido = session.query(ItemPedido).filter_by(SKU = del_sku).first()

        if not del_item:
            print("Item não encontrado!")

        if not del_itens_pedido:
            session.delete(del_item)
            session.commit()

            limpar_tela()
            print(f"""Item deletado: 
    SKU: {del_item.SKU}
    Nome: {del_item.Nome_do_Item}
    Marca: {del_item.Marca}""")
        else:
            limpar_tela()

            """Itens já atribuidos a pedidos não podem ser apagados para não deixar o banco com valores nulls"""
            print("Impossível excluir item, já atribuído a um pedido")