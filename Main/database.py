from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#Criando o banco de dados(sqlite) com nome Catalogo, e atribuindo a variável engine
engine = create_engine('sqlite:///Catalogo.db')

#Criando uma base de sessão que será usada para interagir com o banco
Session = sessionmaker(bind=engine)

#Instância a Sessão
session = Session()

# Cria uma classe base para definir o banco de dados com mapeamento do sqlalchemy
Base = declarative_base ()

#Criando um modelo padrão para que seja possível utilizar a relação 1 para muitos 1:N
class ModeloBase(Base):
    __abstract__ = True
    __allow_unmapped__ = True