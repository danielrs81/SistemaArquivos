import os
from tkinter import messagebox
import re
import configparser

# Carregar configurações
config = configparser.ConfigParser()
config.read('config.ini')

# Definir caminho do arquivo de clientes
CLIENTES_FILE = config.get('PATHS', 'CLIENTES_FILE', fallback=os.path.join("clientes.txt"))

def validar_nome_cliente(nome):
    """Valida se o nome contém apenas letras, espaços e caracteres básicos"""
    if not nome.strip():
        return False, "O nome não pode estar vazio!"
    if re.search(r'[0-9\\\/:*?"<>|]', nome):
        return False, "Nome inválido! Não pode conter números ou caracteres especiais."
    return True, ""

def obter_clientes():
    """Retorna lista de clientes cadastrados em ordem alfabética"""
    try:
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(CLIENTES_FILE), exist_ok=True)
        
        # Criar arquivo se não existir
        if not os.path.exists(CLIENTES_FILE):
            with open(CLIENTES_FILE, 'w', encoding='utf-8') as f:
                pass
        
        with open(CLIENTES_FILE, "r", encoding='utf-8') as f:
            clientes = [linha.strip() for linha in f.readlines() if linha.strip()]
            return sorted(clientes, key=str.lower)
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao carregar clientes: {str(e)}")
        return []

def adicionar_cliente(novo_cliente):
    """Adiciona novo cliente (convertido para maiúsculas)"""
    clientes = obter_clientes()
    novo_cliente = novo_cliente.strip().upper()
    
    valido, msg = validar_nome_cliente(novo_cliente)
    if not valido:
        return False, msg
        
    if not novo_cliente:
        return False, "O nome do cliente não pode estar vazio!"
    if novo_cliente in clientes:
        return False, "Este cliente já está cadastrado!"
    
    try:
        with open(CLIENTES_FILE, "a", encoding='utf-8') as f:
            f.write(novo_cliente + "\n")
        return True, "Cliente cadastrado com sucesso!"
    except Exception as e:
        return False, f"Erro ao cadastrar cliente: {str(e)}"

def remover_cliente(nome_cliente):
    """Remove um cliente existente"""
    clientes = obter_clientes()
    nome_cliente = nome_cliente.strip().upper()
    
    if nome_cliente not in clientes:
        return False, "Cliente não encontrado!"
    
    try:
        with open(CLIENTES_FILE, "w", encoding='utf-8') as f:
            for cliente in clientes:
                if cliente != nome_cliente:
                    f.write(cliente + "\n")
        
        return True, "Cliente removido com sucesso!"
    except Exception as e:
        return False, f"Erro ao remover cliente: {str(e)}"