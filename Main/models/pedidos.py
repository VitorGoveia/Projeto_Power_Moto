from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import ModeloBase, session, Base
from Utilidades.Funcoes import limpar_tela

from models.clientes import Cliente
from models.item import Item
from models.item_pedido import Item_Pedido

#Tabela de associação Pedido e Item_Pedido
pedido_item_associacao = Table(
    'pedido_item_associacao', Base.metadata,
    Column('id_pedido', Integer, ForeignKey('pedidos.id_Pedido')),
    Column('id_itemPedido', Integer, ForeignKey('item_pedido.id_itemPedido'))
)

#Criando Instâncias:
cliente_instancia = Cliente()
itemPedido_instancia = Item_Pedido()

# Tabela de Pedido:

class Pedido(ModeloBase):
    __tablename__ = 'pedidos'

    id_Pedido = Column(Integer, primary_key=True, autoincrement=True)
    Telefone_Cliente = Column(Integer, ForeignKey("cliente.Telefone"))

    cliente = relationship("Cliente", backref="pedidos")
    itens_pedido = relationship("Item_Pedido", secondary=pedido_item_associacao, backref="pedidos")

    def Criar_pedido(self):
        # Atribuir cliente
        Atribui_cliente = input("Digite o número do cliente do orçamento: ")
        while True:
            Cliente_orc = session.query(Cliente).filter_by(Telefone=Atribui_cliente).first()
            if Cliente_orc:
                print(Cliente_orc.Nome)
                break
            else:
                Cadastrar = input("Cliente não encontrado! Deseja cadastrar? (S/N)").upper()
                if Cadastrar[0] == "S":
                    cliente_instancia.adicionar_cliente()
                else:
                    Atribui_cliente = input("Digite novamente o número do cliente do orçamento: ")

        # Criando um novo pedido e adicionando à sessão
        novo_pedido = Pedido(Telefone_Cliente=Cliente_orc.Telefone)
        session.add(novo_pedido)
        session.commit()  # Garante que o pedido já tenha um ID antes de adicionar itens

        print("Atribuindo itens ao orçamento")
        while True:
            # Criando um item do pedido
            Id_criado = itemPedido_instancia.criar_itens_pedido()
            Item_Pedido_Criado = session.query(Item_Pedido).filter_by(id_itemPedido=Id_criado).first()

            # 🔹 Verificar se o item foi encontrado
            if not Item_Pedido_Criado:
                print("Erro ao encontrar o item do pedido.")
                return

            # 🔹 Adicionando o item ao pedido corretamente
            novo_pedido.itens_pedido.append(Item_Pedido_Criado)
            print()
            print()
            session.add(Item_Pedido_Criado)
            session.commit()  # Confirma a adição do item ao pedido

            Continuar = input("Deseja adicionar mais um item? (S/N)").upper()
            if Continuar[0] != "S":
                print("Finalizando orçamento!")
                break

        # Exibir o pedido

        pedido_instancia = Pedido()
        pedido_instancia.Exibir_Pedido(novo_pedido.id_Pedido)

    def _retornar_lista_id_itens_pedido(self, id_pedido):
        # Buscar os itens do pedido
        itens_pedido = session.query(pedido_item_associacao).filter_by(id_pedido=id_pedido).all()

        if not itens_pedido:
            print("Nenhum item encontrado para este pedido.")
            return

        Lista_ids = []
        for lista_id_item_pedido in itens_pedido:
            Lista_ids.append(lista_id_item_pedido.id_itemPedido)

        return Lista_ids

    def Exibir_Pedido(self, Id_pedido_inserido=None, id_item=None):
        limpar_tela()
        if Id_pedido_inserido is None:
            Id_pedido_inserido = input("Digite o Id pedido: ")
        # Buscar o pedido pelo ID
        pedido = session.query(Pedido).filter_by(id_Pedido=Id_pedido_inserido).first()

        if not pedido:
            print("Pedido não encontrado.")
            return

        # Buscar o cliente associado ao pedido
        cliente = session.query(Cliente).filter_by(Telefone=pedido.Telefone_Cliente).first()

        if not cliente:
            print("Cliente não encontrado.")
            return

        print(f"\n--- Pedido {pedido.id_Pedido} ---")
        print(f"Cliente: {cliente.Nome}")
        print(f"Telefone: {cliente.Telefone}\n")

        for item_pedido in self._retornar_lista_id_itens_pedido(pedido.id_Pedido):
            itemPedido_instancia.exibir_item_pedido(item_pedido, id_item)
        print("--- Fim do Pedido ---\n")

    def Alterar_pedido(self):
        numero_pedido = input("Digite o número do pedido: ")
        while True:
            pedido = session.query(Pedido).filter_by(id_Pedido=numero_pedido).one_or_none()
            if not pedido:
                print("Erro: Nenhum pedido encontrado com esse número!")
                numero_pedido = input("Digite o número do pedido novamente: ")
                continue

            if pedido:
                while True:
                    self.Exibir_Pedido(numero_pedido)
                    try:
                        opcao = int(input("""Escolha o que você deseja alterar no pedido:
                            [ 1 ] Alterar Cliente
                            [ 2 ] Alterar quantidade do Item de Pedido
                            [ 3 ] Excluir item do pedido
                            [ 4 ] Acrescentar item no pedido
                            [ 5 ] Voltar ao página principal
                            Digite aqui: """))
                    except ValueError:
                        limpar_tela()
                        print(
                            "Oops! Parece que você digitou um caractere que não é um número, por favor tente de novo.")
                        continue

                    if opcao == 1:
                        cliente_instancia.exibir_cliente(pedido.Telefone_Cliente)
                        try:
                            opcao_cliente = int(input("""O que você deseja alterar no cliente?
                                [ 1 ] O cliente atribuído no pedido
                                [ 2 ] O nome do cliente (manter o número)
                                Digite aqui:"""))
                            if opcao_cliente == 1:
                                pedido.Telefone_Cliente = input("Digite o telefone do novo cliente: ")

                                print("\nCliente alterado com sucesso!")
                            elif opcao_cliente == 2:
                                cliente_instancia.Alterar_cliente(pedido.Telefone_Cliente)
                        except ValueError:
                            limpar_tela()
                            print(
                                "Oops! Parece que você digitou um caractere que não é um número, por favor tente de novo.")
                            continue

                    elif opcao == 2:  # Trocar a quantidade de algum item do pedido
                        try:
                            limpar_tela()
                            self.Exibir_Pedido(numero_pedido, "sim")
                            id_item_pedido = int(input("Digite o id do item que você deseja alterar: "))

                            # Buscando a lista de id_item_pedido:
                            lista_id_pedidos = self._retornar_lista_id_itens_pedido(numero_pedido)

                            if id_item_pedido is None:
                                break

                            if id_item_pedido not in lista_id_pedidos:
                                print("Deu ruim")

                            itemPedido_instancia.alterar_item_pedido(id_item_pedido)

                        except ValueError:
                            limpar_tela()
                            print(
                                "Oops! Parece que você digitou um caractere que não é um número, por favor tente de novo.")
                            continue

                    elif opcao == 3:  # Excluir item do pedido
                        pass

                    elif opcao == 4:  # Adicionar item no pedido
                        pass

                    elif opcao == 5:
                        break

                    else:
                        print("Número inválido")

                session.commit()
                limpar_tela()
                print("Alterações feitas com sucesso!")
                print()
                break

        # POSSO CRIAR UMA LISTA COM TODOS OS ID DO ITEM DO PEDIDO e depois chamar na query com um for, então a função exibir deve receber uma lista e não um ID apenas