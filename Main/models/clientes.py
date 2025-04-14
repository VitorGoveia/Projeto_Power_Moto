from database import ModeloBase, session
from sqlalchemy import Column, String
from Utilidades.Funcoes import limpar_tela

class Cliente(ModeloBase):
    __tablename__ = 'cliente'

    Nome = Column(String)
    Telefone = Column(String, primary_key=True)

    def adicionar_cliente(self):
        Nome_cliente = input("Digite o nome do cliente a ser cadastrado: ")
        Telefone_cliente = input("Digite o telefone (somente número): ")

        criar_cliente = session.query(Cliente).filter_by(Telefone=Telefone_cliente).first()
        if not criar_cliente:
            criar_cliente = Cliente(Nome=Nome_cliente,
                                    Telefone=Telefone_cliente)
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

    def exibir_cliente(self, Tel_cliente=None):  # Funçao somente para exibir os itens
        limpar_tela()
        if Tel_cliente is None:
            Tel_cliente = input("Digite o Telefone a ser verificado (não digite nada para todos): ")

        if Tel_cliente:
            Cli = session.query(Cliente).filter_by(Telefone=Tel_cliente).first()
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
                    print()
                    limpar_tela()
                    print("Alteração feita com sucesso!")
                    print()
                    break
                break
            else:
                tel_cliente = input("Item não existe! Digite novamente: ")
                if not tel_cliente:
                    break
