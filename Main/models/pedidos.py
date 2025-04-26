from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import ModeloBase, session, Base
from Utilidades.Funcoes import limpar_tela

from models.clientes import Cliente
from models.item_pedido import ItemPedido

#Tabela de associação Pedido e ItemPedido
pedido_item_associacao = Table(
    'pedido_item_associacao', Base.metadata,
    Column('id_pedido', Integer, ForeignKey('pedidos.id_Pedido')),
    Column('id_itemPedido', Integer, ForeignKey('item_pedido.id_itemPedido'))
)

#Criando Instâncias:
cliente_instancia = Cliente()
itemPedido_instancia = ItemPedido()

# Tabela de Pedido:

class Pedido(ModeloBase):
    __tablename__ = 'pedidos'

    id_Pedido = Column(Integer, primary_key=True, autoincrement=True)
    Telefone_Cliente = Column(Integer, ForeignKey("cliente.Telefone"))

    cliente = relationship("Cliente", backref="pedidos")
    itens_pedido = relationship("ItemPedido", secondary=pedido_item_associacao, backref="pedidos")

    def Criar_pedido(self):
        # Atribuir cliente
        atribui_cliente = input("Digite o número do cliente do orçamento: ")
        while True:
            cliente_orc = session.query(Cliente).filter_by(Telefone=atribui_cliente).first()
            if cliente_orc:
                print(cliente_orc.Nome)
                break
            else:
                cadastrar = input("Cliente não encontrado! Deseja cadastrar? (S/N)").upper()
                if cadastrar[0] == "S":
                    cliente_instancia.adicionar_cliente()
                else:
                    atribui_cliente = input("Digite novamente o número do cliente do orçamento: ")

        # Criando um pedido e adicionando à sessão
        novo_pedido = Pedido(Telefone_Cliente=cliente_orc.Telefone)
        session.add(novo_pedido)
        session.commit()  # Garante que o pedido já tenha um ID antes de adicionar itens

        print("Atribuindo itens ao orçamento, para finalizar basta não digitar a SKU!")
        while True:
            # Criando um item do pedido
            id_criado = itemPedido_instancia.criar_itens_pedido()
            item_Pedido_Criado = session.query(ItemPedido).filter_by(id_itemPedido=id_criado).first()

            if not id_criado:
                print("Finalizando orçamento!")
                break

            # 🔹 Verificar se o item foi encontrado
            if not item_Pedido_Criado:
                print("Erro ao encontrar o item do pedido.")
                return

            # 🔹 Adicionando o item ao pedido corretamente
            novo_pedido.itens_pedido.append(item_Pedido_Criado)
            print()
            session.add(item_Pedido_Criado)
            session.commit()  # Confirma a adição do item ao pedido

        # Exibir o pedido

        pedido_instancia = Pedido()
        pedido_instancia.Exibir_Pedido(novo_pedido.id_Pedido)

    def _retornar_lista_id_itens_pedido(self, id_pedido):
        # Buscar os itens do pedido
        itens_pedido = session.query(pedido_item_associacao).filter_by(id_pedido=id_pedido).all()

        if not itens_pedido:
            print("Nenhum item encontrado para este pedido.")
            return None

        lista_ids = []
        for lista_id_item_pedido in itens_pedido:
            lista_ids.append(lista_id_item_pedido.id_itemPedido)

        return lista_ids

    def Exibir_Pedido(self, id_pedido_inserido=None, id_item=None):
        limpar_tela()
        if id_pedido_inserido is None:
            id_pedido_inserido = input("Digite o Id pedido: ")
        # Buscar o pedido pelo "ID"
        pedido = session.query(Pedido).filter_by(id_Pedido=id_pedido_inserido).first()

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

        valor_total = 0
        for item_pedido in self._retornar_lista_id_itens_pedido(pedido.id_Pedido):
            itemPedido_instancia.exibir_item_pedido(item_pedido, id_item)
            valor_total += itemPedido_instancia.retorna_valor(item_pedido)

        print(f"Total: {str(valor_total)}\n".replace(".",","))
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
                            [ 2 ] Alterar quantidade ou prazo do Item de Pedido
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
                        self.Exibir_Pedido(numero_pedido, "sim")

                        del_id_item_pedido = input("Digite o Id do item que será retirado: ")
                        itemPedido_instancia.deletar_item_pedido(del_id_item_pedido)
                        limpar_tela()

                        self.Exibir_Pedido(numero_pedido, "sim")

                    elif opcao == 4:  # Adicionar item no pedido
                        self.Exibir_Pedido(numero_pedido)

                        print("Adicionar novo item no pedido:")

                        resgatar_pedido = session.query(Pedido).filter_by(id_Pedido=numero_pedido).one_or_none()

                        while True:
                            # Criando um item do pedido
                            adicionando_item = itemPedido_instancia.criar_itens_pedido()
                            adicionando_item_pedido = session.query(ItemPedido).filter_by(id_itemPedido=adicionando_item).first()

                            # 🔹 Verificar se o item foi encontrado
                            if not adicionando_item_pedido:
                                print("Erro ao encontrar o item do pedido.")
                                return

                            resgatar_pedido.itens_pedido.append(adicionando_item_pedido)
                            print()
                            session.add(adicionando_item_pedido)
                            session.commit()  # Confirma a adição do item ao pedido

                            continuar = input("Deseja adicionar mais um item? (S/N)").upper()
                            if continuar[0] != "S":
                                print("Finalizando orçamento!")
                                break

                        # Exibir o pedido atualizado

                        limpar_tela()
                        print("Pedido atualizado: ")
                        self.Exibir_Pedido(numero_pedido)

                    elif opcao == 5:
                        break

                    else:
                        print("Número inválido")

                session.commit()
                limpar_tela()
                print("Alterações feitas com sucesso!")
                print()
                break

    def deletar_pedido(self):
        del_id_pedido = int(input("Digite o id do pedido que será deletado: "))
        del_pedido = session.query(Pedido).filter_by(id_Pedido = del_id_pedido).first()

        self.Exibir_Pedido(del_id_pedido)
        confirma = input("\nVocê tem certeza que deseja deletar o pedido? (S/N) ").upper()

        if not del_pedido:
            print("Pedido não encontrado")

        if confirma[0] == "S":
            del_itens_pedido = session.query(pedido_item_associacao).filter_by(id_pedido = del_id_pedido).all()

            for item_pedido in del_itens_pedido:
                itemPedido_instancia.deletar_item_pedido(item_pedido.id_itemPedido)

            session.delete(del_pedido)

            session.commit()

        print(f"""Orçamento {del_id_pedido} deletado!""")