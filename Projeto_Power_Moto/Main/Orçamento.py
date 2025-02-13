from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

#Criando o banco de dados(sqlite) com nome Catalogo, e atribuindo a variável engine
engine = create_engine('sqlite:///Catalogo.db') 

#Criando uma base de sessão que será usada para interagir com o banco
Session = sessionmaker(bind=engine)

#Instância a Sessão
session = Session()


Base = declarative_base () # Cria uma classe base para definir o banco de dados com mapeamento do sqlalchemy  
#Criando as tabelas:

#Tabela de Item:

class Item(Base):
    __tablename__ = 'itens'

    SKU = Column(String, primary_key = True)
    Valor_Unitario = Column(Numeric(10,2))
    Nome_do_Item = Column(String) 
    Marca = Column(String)

    def adicionar_item(self,SKU_item, Nome, Valor, Marca_item):
        criar_item = session.query(Item).filter_by(SKU=SKU_item).first()
        if not criar_item:
            criar_item = Item(SKU=SKU_item,
                              Nome_do_Item = Nome,
                              Valor_Unitario = Valor,
                              Marca = Marca_item)
            session.add(criar_item)
            session.commit()
            print("Item adicionado com sucesso")
            print()
            return
        print("Já há um item com essa SKU!")

    def exibir_item(self):  # Funçao somente para exibir os itens
        itens = session.query(Item).all()
        print('Esses são todos os itens em nosso Banco de Dados:')
        for item_loop in itens:  # percorre o conjunto de matérias
            print()
            print(f'{item_loop.Nome_do_Item} ({item_loop.SKU})')
            print(f'Valor: R${item_loop.Valor_Unitario}')
            print(f'Marca: {item_loop.Marca}')
            print()

#Tabela de Cliente:

class Cliente(Base):
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

    def exibir_cliente(self):  # Funçao somente para exibir os itens
        Tel_cliente = input("Digite o Telefone a ser verificado (não digite nada para todos): ")

        if Tel_cliente:
            Cli = session.query(Cliente).filter_by(Telefone = Tel_cliente).first()
            if Cli:
                print()
                print(f'Nome: {Cli.Nome}')
                print(f'Telefone: {Cli.Telefone}')
                print()
                return
            else:
                print()
                print("Cliente não encontrado")
                print()
                return
        else:
            Cli = session.query(Cliente).all()
            for cliente_dado in Cli:  # percorre o conjunto de matérias
                print()
                print(f'Nome: {cliente_dado.Nome}')
                print(f'Telefone: {cliente_dado.Telefone}')
                print()
            
#Tabela de Item_pedido:

class Item_Pedido(Base):
    __tablename__ = 'item_pedido'

    id_itemPedido = Column(Integer, primary_key = True, autoincrement=True) 
    quantidade = Column(Integer)
    Valor_ItemPedido = Column(Numeric(10,2))
    SKU = Column(String, ForeignKey("itens.SKU"))
    Prazo_Pedido = Column(Integer)

    item = relationship('Item', backref='item_pedido')
    
#Tabela de Pedido:

class Pedido(Base):
    __tablename__ = 'pedidos'

    id_Pedido = Column(Integer, primary_key=True, autoincrement=True) 
    Telefone = Column(Integer, ForeignKey("cliente.Telefone"))  # Relacionado a Cliente
    id_itemPedido = Column(Integer, ForeignKey("item_pedido.id_itemPedido"))  # Relacionado a Item_Pedido

    cliente = relationship("Cliente", backref="pedidos")
    item_pedido = relationship("Item_Pedido", backref="pedidos")

Base.metadata.create_all(engine)  # Cria todas as tabelas definidas na classe base no banco de dados, se ainda não existirem

while True:  # menu interativo
    try:
        opcao = int(input("""Escolha uma opção:
        [ 1 ] Realizar orçamento
        [ 2 ] Adicionar Item
        [ 3 ] Exibir Item
        [ 4 ] Deletar Item
        [ 5 ] Alterar Orçamento
        Digite aqui: """))
    except ValueError:
        print("Oops! Parece que você digitou um caractere que não é um número, por favor tente de novo.")
        continue

    #Instânciando as tabelas
    item_instancia = Item()
    cliente_instancia = Cliente()

    if opcao == 1:
        cliente_instancia.adicionar_cliente()
        cliente_instancia.exibir_cliente()
        
    elif opcao == 2:
        SKU = input('Digite a SKU do item: ')
        Nome = input('Digite o nome do item: ')
        Valor = float(input('Agora digite o valor unitário do item (com .):'))
        Marca = input('Digite a marca do item: ')

        item_instancia.adicionar_item(SKU, Nome, Valor, Marca)

    elif opcao == 3:
        item_instancia.exibir_item()
