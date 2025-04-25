from Utilidades.Funcoes import limpar_tela
from database import ModeloBase, session
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, desc
from sqlalchemy.orm import relationship
from models.item import Item  # Para validar SKU

item_instancia = Item()

class Item_Pedido(ModeloBase):
    __tablename__ = 'item_pedido'

    id_itemPedido = Column(Integer, primary_key=True, autoincrement=True)
    quantidade = Column(Integer)
    Valor_ItemPedido = Column(Numeric(10, 2))
    SKU = Column(String, ForeignKey("itens.SKU"))
    Prazo_Pedido = Column(Integer)

    item = relationship('Item', backref='item_pedido')

    def criar_itens_pedido(self):
        while True:
            sku_item = input("Digite a SKU do item: ")
            Valida_Sku = session.query(Item).filter_by(SKU=sku_item).first()
            if Valida_Sku:
                break
            print("Item não encontrado, favor cadastrar:")

            item_instancia.Adicionar_Item()

        Quantidade_Item_Pedido = int(input("Digite a quantidade do item: "))
        Valor_Item_Pedido = Valida_Sku.Valor_Unitario * Quantidade_Item_Pedido
        Prazo = int(input("Digite o prazo máximo (em dias): "))

        Criar_Item = Item_Pedido(SKU=Valida_Sku.SKU,
                                 quantidade=Quantidade_Item_Pedido,
                                 Valor_ItemPedido=Valor_Item_Pedido,
                                 Prazo_Pedido=Prazo)
        session.add(Criar_Item)
        session.commit()

        # Retornando o id para adicionar ao orçamento
        Return_Id_session = session.query(Item_Pedido).order_by(desc(Item_Pedido.id_itemPedido)).first()
        Return_Id = Return_Id_session.id_itemPedido

        return Return_Id

    def exibir_item_pedido(self, item_pedido, id_item=None): #id
        Buscar_iP = session.query(Item_Pedido).filter_by(id_itemPedido=item_pedido).first()
        item = session.query(Item).filter_by(SKU=Buscar_iP.SKU).first()

        if not item:
            print(f"Item com SKU {Buscar_iP.SKU} não encontrado.")

        quantidade = Buscar_iP.quantidade
        descricao_quantidade = f"{quantidade} UNIDADE" if quantidade == 1 else f"{quantidade} UNIDADES"

        if id_item is not None:
            print(f"Id do item: {Buscar_iP.id_itemPedido}")

        print(f"{item.Nome_do_Item} ({item.SKU}) - {descricao_quantidade}")
        print(f"Valor: R$ {Buscar_iP.Valor_ItemPedido:.2f}")

        # Exibir o prazo de entrega
        if Buscar_iP.Prazo_Pedido == 0:
            print("Prazo: À pronta entrega\n")
        elif Buscar_iP.Prazo_Pedido == 7:
            print("Prazo estimado: 7 dias (transferência)\n")
        else:
            print(f"Prazo estimado: {Buscar_iP.Prazo_Pedido} dias úteis (encomenda)\n")

    def alterar_item_pedido(self, id_itemPedido_externo):
        item_pedido = session.query(Item_Pedido).filter_by(id_itemPedido = id_itemPedido_externo).first()
        item_atribuido = session.query(Item).filter_by(SKU = item_pedido.SKU).first()
        limpar_tela()
        self.exibir_item_pedido(item_pedido.id_itemPedido)

        try:
            opcao = int(input("""O que você deseja alterar? 
            [ 1 ] Quantidade 
            [ 2 ] Prazo
            """))

            if opcao == 1:
                quantidade = int(input("Digite quantos itens serão atribuidos: "))
                item_pedido.quantidade = quantidade
                item_pedido.Valor_ItemPedido = quantidade * item_atribuido.Valor_Unitario

            if opcao == 2:
                prazo = int(input("Digite o novo prazo em dias: "))
                item_pedido.Prazo_Pedido = prazo

        except ValueError:
            limpar_tela()
            print(
                "Oops! Parece que você digitou um caractere que não é um número, por favor tente de novo.")

        session.commit()
        print("\n Alteração feita com sucesso!")
