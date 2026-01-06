"""
Script standalone para criar as tabelas do banco de dados.
Execute este script após fazer deploy para inicializar o banco.
"""
import sys
import os

# Adiciona o diretório backend ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.init_db import init_db

if __name__ == "__main__":
    print("=" * 60)
    print("Criando tabelas no banco de dados...")
    print("=" * 60)
    
    try:
        init_db()
        print("\n" + "=" * 60)
        print("✓ Banco de dados inicializado com sucesso!")
        print("=" * 60)
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"✗ Erro ao inicializar banco de dados: {str(e)}")
        print("=" * 60)
        sys.exit(1)
