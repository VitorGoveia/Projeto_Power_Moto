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

    def Adicionar_Item(self):
        sku_item = input('Digite a SKU do item: ')
        Nome = input('Digite o nome do item: ')
        Valor = float(input('Agora digite o valor unitário do item (com .):'))
        Marca_item = input('Digite a marca do item: ')

        criar_item = session.query(Item).filter_by(SKU=sku_item).first()
        if criar_item:
            print("Já há um item com essa SKU!")
        else:
            criar_item = Item(SKU=sku_item,
                              Nome_do_Item=Nome,
                              Valor_Unitario=Valor,
                              Marca=Marca_item)
            session.add(criar_item)
            session.commit()
            print("Item adicionado com sucesso")
            print()

    # Função de exibir os detalhes -- evitar repetição de códigos
    def _Exibir_detalhes_itens(self, item):
        print()
        print(f'{item.Nome_do_Item} ({item.SKU})')
        print(f'Valor: R${item.Valor_Unitario}')
        print(f'Marca: {item.Marca}')
        print()

        # Funçao somente para exibir os itens

    def Exibir_item(self):
        limpar_tela()
        buscar = input("Digite a SKU do item ou deixe em branco para todos: ")
        if buscar:
            while True:
                item = session.query(Item).filter_by(SKU=buscar).first()
                if item:
                    self._Exibir_detalhes_itens(item)
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
                print('Esses são todos os itens em nosso Banco de Dados:')
                for item in itens:  # percorre o conjunto de matérias
                    self._Exibir_detalhes_itens(item)

    # Funçao somente para alterar um item:
    def Alterar_item(self):
        buscar = input("Digite a SKU do item que será alterado: ")
        while True:
            item = session.query(Item).filter_by(SKU=buscar).one_or_none()
            if not item:
                print("Erro: Nenhum item encontrado com essa SKU!")
            else:
                self._Exibir_detalhes_itens(item)
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
