from Utilidades.Funcoes import limpar_tela
from database import ModeloBase, session
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, desc
from sqlalchemy.orm import relationship
from models.item import Item  # Para validar SKU

item_instancia = Item()

class ItemPedido(ModeloBase):
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

            if not sku_item:
                return None

            valida_sku = session.query(Item).filter_by(SKU=sku_item).first()
            if valida_sku:
                break
            print("Item não encontrado, favor cadastrar:")

            item_instancia.Adicionar_Item()

        while True:
            quantidade_item_pedido = int(input("Digite a quantidade do item: "))
            if quantidade_item_pedido == 0:
                print("Impossível a quantidade ser 0, digite novamente!\n")
            else:
                break

        valor_item_pedido = valida_sku.Valor_Unitario * quantidade_item_pedido
        prazo = int(input("Digite o prazo máximo (em dias): "))

        criar_item = ItemPedido(SKU=valida_sku.SKU,
                                 quantidade=quantidade_item_pedido,
                                 Valor_ItemPedido=valor_item_pedido,
                                 Prazo_Pedido=prazo)
        session.add(criar_item)
        session.commit()

        # Retornando o "id" para adicionar ao orçamento
        return_id_session = session.query(ItemPedido).order_by(desc(ItemPedido.id_itemPedido)).first()
        return_id = return_id_session.id_itemPedido

        return return_id

    def exibir_item_pedido(self, item_pedido, id_item=None): #id
        buscar_ip = session.query(ItemPedido).filter_by(id_itemPedido=item_pedido).first()
        item = session.query(Item).filter_by(SKU=buscar_ip.SKU).first()

        if not item:
            print(f"Item com SKU {buscar_ip.SKU} não encontrado.")

        quantidade = buscar_ip.quantidade
        descricao_quantidade = f"{quantidade} UNIDADE" if quantidade == 1 else f"{quantidade} UNIDADES"

        if id_item is not None:
            print(f"Id do item: {buscar_ip.id_itemPedido}")

        print(f"{item.Nome_do_Item} ({item.SKU}) - {descricao_quantidade}")
        print(f"Valor: R$ {buscar_ip.Valor_ItemPedido:.2f}".replace('.', ','))

        # Exibir o prazo de entrega
        if buscar_ip.Prazo_Pedido == 0:
            print("Prazo: À pronta entrega\n")
        elif buscar_ip.Prazo_Pedido == 7:
            print("Prazo estimado: 7 dias (transferência)\n")
        else:
            print(f"Prazo estimado: {buscar_ip.Prazo_Pedido} dias úteis (encomenda)\n")

    def alterar_item_pedido(self, id_item_pedido_externo):
        item_pedido = session.query(ItemPedido).filter_by(id_itemPedido = id_item_pedido_externo).first()
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

    def deletar_item_pedido(self, del_id_item_pedido = None):
        if del_id_item_pedido is None:
            del_id_item_pedido = int(input("Digite o id do item que será deletado: "))

        del_item_pedido = session.query(ItemPedido).filter_by(id_itemPedido = del_id_item_pedido).first()

        session.delete(del_item_pedido)
        session.commit()

    def retorna_valor(self, id_item_pedido):
        item_pedido_val = session.query(ItemPedido).filter_by(id_itemPedido = id_item_pedido).first()
        return item_pedido_val.Valor_ItemPedido