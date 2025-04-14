import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
    # Verifica o sistema operacional:
    # - Se for Windows (os.name == 'nt'), executa o comando 'cls'
    # - Caso contrário (Linux ou macOS), executa o comando 'clear'