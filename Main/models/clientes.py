from database import ModeloBase, session
from sqlalchemy import Column, String
from Utilidades.Funcoes import limpar_tela

class Cliente(ModeloBase):
    __tablename__ = 'cliente'

    Nome = Column(String)
    Telefone = Column(String, primary_key=True)

    def adicionar_cliente(self):
        nome_cliente = input("Digite o nome do cliente a ser cadastrado: ")
        telefone_cliente = input("Digite o telefone (somente número): ")

        criar_cliente = session.query(Cliente).filter_by(Telefone=telefone_cliente).first()
        if not criar_cliente:
            criar_cliente = Cliente(Nome=nome_cliente,
                                    Telefone=telefone_cliente)
            session.add(criar_cliente)
            session.commit()
            print("Cliente cadastrado!")
            print()
            return
        print("Telefone já cadastrado")

    def _Exibir_detalhes_cliente(self, tel):
        print(f"Nome: {tel.Nome}")
        print(f"Telefone {tel.Telefone}\n")

    def exibir_cliente(self, tel_cliente=None):  # Funçao somente para exibir os itens
        limpar_tela()
        if tel_cliente is None:
            tel_cliente = input("Digite o Telefone a ser verificado (não digite nada para todos): ")

        if tel_cliente:
            cli = session.query(Cliente).filter_by(Telefone=tel_cliente).first()
            if cli:
                self._Exibir_detalhes_cliente(cli)
                return
            else:
                print()
                print("Cliente não encontrado")
                print()
                return
        else:
            cli = session.query(Cliente).all()
            for cliente_dado in cli:  # percorre o conjunto de matérias
                self._Exibir_detalhes_cliente(cliente_dado)

    def Alterar_cliente(self, tel_cliente=None):
        if tel_cliente is None:
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
                        cliente.Nome = input("Digite o novo nome do cliente: ")
                    elif opcao[0] == "N":
                        print(
                            "O telefone é um atributo imutável, caso você deseje esse cliente com um novo número, será preciso criar um novo cadastro!")
                        return
                    else:
                        print("Nenhum valor um válido foi digitado!")
                        return

                    session.commit()
                    limpar_tela()
                    print("\nAlteração feita com sucesso!\n")
                    break
                break
            else:
                tel_cliente = input("Item não existe! Digite novamente: ")
                if not tel_cliente:
                    break

    def Deletar_cliente(self):
        from models.pedidos import Pedido
        del_telefone = input("Digite o telefone do cliente que será deletado: ")

        del_cliente = session.query(Cliente).filter_by(Telefone = del_telefone).first()
        del_pedido = session.query(Pedido).filter_by(Telefone_Cliente = del_telefone).first()

        if not del_cliente:
            print("Cliente não encontrado")

        if not del_pedido:
            session.delete(del_cliente)
            session.commit()

            limpar_tela()
            print(f"""Cliente deletado: 
    Telefone: {del_cliente.Telefone}
    Nome: {del_cliente.Nome}""")
        else:
            limpar_tela()
            print("Impossível excluir cliente, já atribuído a um pedido")