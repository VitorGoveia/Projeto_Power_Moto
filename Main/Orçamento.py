from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric, Table, desc
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

#Criando o banco de dados(sqlite) com nome Catalogo, e atribuindo a variável engine
engine = create_engine('sqlite:///Catalogo.db') 

#Criando uma base de sessão que será usada para interagir com o banco
Session = sessionmaker(bind=engine)

#Instância a Sessão
session = Session()

Base = declarative_base () # Cria uma classe base para definir o banco de dados com mapeamento do sqlalchemy  
#Criando as tabelas:

pedido_item_associacao = Table(
    'pedido_item_associacao', Base.metadata,
    Column('id_pedido', Integer, ForeignKey('pedidos.id_Pedido')),
    Column('id_itemPedido', Integer, ForeignKey('item_pedido.id_itemPedido'))
)

#Criando um modelo padrão para que seja possível utilizar a relação 1 para muitos 1:N

class Modelo_Base(Base):
    __abstract__ = True
    __allow_unmapped__ = True

#Tabela de Item:

class Item(Modelo_Base):
    __tablename__ = 'itens'

    SKU = Column(String, primary_key = True)
    Valor_Unitario = Column(Numeric(10,2))
    Nome_do_Item = Column(String) 
    Marca = Column(String)

    def Adicionar_Item(self):
        SKU_item = input('Digite a SKU do item: ')
        Nome = input('Digite o nome do item: ')
        Valor = float(input('Agora digite o valor unitário do item (com .):'))
        Marca_item = input('Digite a marca do item: ')
        
        criar_item = session.query(Item).filter_by(SKU=SKU_item).first()
        if criar_item:
            print("Já há um item com essa SKU!")
        else:
            criar_item = Item(SKU=SKU_item,
                                Nome_do_Item = Nome,
                                Valor_Unitario = Valor,
                                Marca = Marca_item)
            session.add(criar_item)
            session.commit()
            print("Item adicionado com sucesso")
            print()

    #Função de exibir os detalhes -- evitar repetição de códigos
    def _Exibir_detalhes_itens(self, item):
        print()
        print(f'{item.Nome_do_Item} ({item.SKU})')
        print(f'Valor: R${item.Valor_Unitario}')
        print(f'Marca: {item.Marca}')
        print()    

    # Funçao somente para exibir os itens
    def Exibir_item(self):  
        buscar = input("Digite a SKU do item ou deixe em branco para todos: ")
        if buscar:
            while True:
                item = session.query(Item).filter_by(SKU = buscar).first()
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
                    self._exibir_detalhes_itens(item)

    # Funçao somente para alterar um item:
    def Alterar_item(self):
        buscar = input("Digite a SKU do item que será alterado: ")
        while True:
            item = session.query(Item).filter_by(SKU = buscar).one_or_none()
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
                    print("Alteração feita com sucesso!")
                    print()
                    break
                    
                break
            else:
                buscar = input("Item não existe! Digite novamente: ")
                if not buscar:
                    break

#Tabela de Cliente:

class Cliente(Modelo_Base):
    __tablename__ = 'cliente'

    Nome = Column(String)
    Telefone = Column(String, primary_key = True)

    def adicionar_cliente(self):
        Nome_cliente = input("Digite o nome do cliente a ser cadastrado: ")
        Telefone_cliente = input("Digite o telefone (somente número): ")
        
        criar_cliente = session.query(Cliente).filter_by(Telefone = Telefone_cliente).first()
        if not criar_cliente:
            criar_cliente = Cliente(Nome = Nome_cliente,
                                    Telefone = Telefone_cliente)
            session.add(criar_cliente)
            session.commit()
            print("Cliente cadastrado!")
            print()
            return
        print("Telefone já cadastrado")

    def _Exibir_detalhes_cliente(self, tel):
        print()
        print(f"Nome: {tel.Nome}")
        print(f"Telefone {tel.Telefone}")
        print()

    def exibir_cliente(self):  # Funçao somente para exibir os itens
        Tel_cliente = input("Digite o Telefone a ser verificado (não digite nada para todos): ")

        if Tel_cliente:
            Cli = session.query(Cliente).filter_by(Telefone = Tel_cliente).first()
            if Cli:
                self._Exibir_detalhes_cliente(Cli)
                return
            else:
                print()
                print("Cliente não encontrado")
                print()
                return
        else:
            Cli = session.query(Cliente).all()
            for cliente_dado in Cli:  # percorre o conjunto de matérias
                self._Exibir_detalhes_cliente(cliente_dado)


    def Alterar_cliente(self):
        tel_cliente = input("Digite o telefone do cliente que será alterado: ")
        while True:
            cliente = session.query(Cliente).filter_by(Telefone=tel_cliente).one_or_none()
            if not cliente:
                print("Erro: Nenhum cliente encontrado com esse telefone!")
            else:
                self._Exibir_detalhes_cliente(cliente)
            if cliente:
                while True:
                    opcao = input("Você deseja alterar o nome? (S/N)").upper()
                    if opcao[0] == "S":
                        cliente.Nome_do_Item = input("Digite o novo nome do cliente: ")
                    elif opcao[0] == "N":
                        print("O telefone é um atributo imutável, caso você deseje esse cliente com um novo número, será preciso criar um novo cadastro!")
                        return
                    else:
                        print("Nenhum valor um válido foi digitado!")
                        return

                    session.commit()
                    print()
                    print("Alteração feita com sucesso!")
                    print()
                    break
                break
            else:
                tel_cliente = input("Item não existe! Digite novamente: ")
                if not tel_cliente:
                    break

#Tabela de Item_pedido:

class Item_Pedido(Modelo_Base):
    __tablename__ = 'item_pedido'

    id_itemPedido = Column(Integer, primary_key = True, autoincrement=True) 
    quantidade = Column(Integer)
    Valor_ItemPedido = Column(Numeric(10,2))
    SKU = Column(String, ForeignKey("itens.SKU"))
    Prazo_Pedido = Column(Integer)

    item = relationship('Item', backref='item_pedido')

    def criar_itens_pedido(self):
        while True:
            Sku_item = input("Digite a SKU do item: ")
            Valida_Sku = session.query(Item).filter_by(SKU = Sku_item).first()
            if Valida_Sku:
                break
            print("Item não encontrado, favor cadastrar:")
            item_instancia.Adicionar_Item()
        Quantidade_Item_Pedido = int(input("Digite a quantidade do item: "))
        Valor_Item_Pedido = Valida_Sku.Valor_Unitario * Quantidade_Item_Pedido
        Prazo = int(input("Digite o prazo máximo (em dias): "))        
        
        Criar_Item = Item_Pedido(SKU = Valida_Sku.SKU,
                                 quantidade = Quantidade_Item_Pedido,
                                 Valor_ItemPedido = Valor_Item_Pedido,
                                 Prazo_Pedido = Prazo)
        session.add(Criar_Item)
        session.commit()

        #Retornando o id para adicionar ao orçamento
        Return_Id_session = session.query(Item_Pedido).order_by(desc(Item_Pedido.id_itemPedido)).first()
        Return_Id = Return_Id_session.id_itemPedido    

        
        return Return_Id

        #Ajustar o if not: Ele não está validando novamente após a criação, realizar testes!
        
#Tabela de Pedido:

class Pedido(Modelo_Base):
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
        pedido_instancia.Exibir_Pedido(novo_pedido.id_Pedido)
        
    def Exibir_Pedido(self, Id_pedido_inserido):
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
        print(f"Telefone: {cliente.Telefone}")
        
        # Buscar os itens do pedido
        itens_pedido = session.query(pedido_item_associacao).filter_by(id_pedido = pedido.id_Pedido).all()
        
        if not itens_pedido:
            print("Nenhum item encontrado para este pedido.")
            return

        Lista_ids = []
        for lista_id_item_pedido in itens_pedido:
            Lista_ids.append(lista_id_item_pedido.id_itemPedido)

        print("\nItens do Pedido:")
        
        for item_pedido in Lista_ids:
            Buscar_iP = session.query(Item_Pedido).filter_by(id_itemPedido = item_pedido).first()
            item = session.query(Item).filter_by(SKU = Buscar_iP.SKU).first()

            if not item:
                print(f"Item com SKU {item_pedido.SKU} não encontrado.")
                continue
            
            quantidade = Buscar_iP.quantidade
            descricao_quantidade = f"{quantidade} UNIDADE" if quantidade == 1 else f"{quantidade} UNIDADES"
            
            print(f"\n{item.Nome_do_Item} ({item.SKU}) - {descricao_quantidade}")
            print(f"Valor: R$ {Buscar_iP.Valor_ItemPedido:.2f}")

            # Exibir o prazo de entrega
            if Buscar_iP.Prazo_Pedido == 0:
                print("Prazo: À pronta entrega")
            elif Buscar_iP.Prazo_Pedido == 7:
                print("Prazo estimado: 7 dias (transferência)")
            else:
                print(f"Prazo estimado: {Buscar_iP.Prazo_Pedido} dias úteis (encomenda)")

        print("\n--- Fim do Pedido ---\n")

        

        #POSSO CRIAR UMA LISTA COM TODOS OS ID DO ITEM DO PEDIDO e depois chamar na query com um for, então a função exibir deve receber uma lista e não um ID apenas
        
        

Base.metadata.create_all(engine)  # Cria todas as tabelas definidas na classe base no banco de dados, se ainda não existirem

while True:  # menu interativo
    try:
        opcao = int(input("""Escolha uma opção:
        [ 1 ] Realizar orçamento
        [ 2 ] Alterar
        [ 3 ] Exibir
        [ 4 ] Deletar
        Digite aqui: """))
    except ValueError:
        print("Oops! Parece que você digitou um caractere que não é um número, por favor tente de novo.")
        continue

    #Instânciando as tabelas
    item_instancia = Item()
    cliente_instancia = Cliente()
    itemPedido_instancia = Item_Pedido()
    pedido_instancia = Pedido()
    
    if opcao == 1:
        pedido_instancia.Criar_pedido()
        
    elif opcao == 2:
        try:
            opcao = int(input("""Escolha uma opção:
            [ 1 ] Alterar Item
            [ 2 ] Alterar Cliente
            [ 3 ] Alterar Pedido
            Digite aqui: """))
        except ValueError:
            print("Oops! Parece que você digitou um caractere que não é um número, por favor tente de novo.")
            continue

        if opcao == 1:
            item_instancia.Alterar_item()
        elif opcao == 2:
            cliente_instancia.Alterar_cliente()

        if opcao == 1:
            item_instancia.Alterar_item()
        elif opcao == 2:
            pass
        elif opcao == 3:
            pass

    elif opcao == 3:
        item_instancia.Exibir_item()

    elif opcao == 4:
        pedido_instancia.Criar_pedido()