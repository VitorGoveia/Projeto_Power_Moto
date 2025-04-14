from database import ModeloBase, session
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, desc
from sqlalchemy.orm import relationship
from models.item import Item  # Para validar SKU

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

            item_instancia = Item()
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

        # Ajustar o if not: Ele não está validando novamente após a criação, realizar testes!