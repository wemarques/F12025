"""
Script para verificar e instalar dependências necessárias.
Execute este script antes de rodar a aplicação.
"""
import sys
import subprocess

def check_and_install(package_name):
    """Verifica se um pacote está instalado e instala se necessário."""
    try:
        __import__(package_name)
        print(f"[OK] {package_name} esta instalado")
        return True
    except ImportError:
        print(f"[AVISO] {package_name} nao encontrado. Instalando...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"[OK] {package_name} instalado com sucesso!")
            return True
        except Exception as e:
            print(f"[ERRO] Erro ao instalar {package_name}: {e}")
            return False

if __name__ == "__main__":
    print("Verificando dependencias...\n")
    print(f"Python: {sys.executable}\n")
    
    packages = ["plotly", "requests", "streamlit", "fastapi", "uvicorn"]
    
    all_ok = True
    for package in packages:
        if not check_and_install(package):
            all_ok = False
    
    print("\n" + "="*50)
    if all_ok:
        print("[OK] Todas as dependencias estao instaladas!")
    else:
        print("[ERRO] Algumas dependencias falharam ao instalar.")
        sys.exit(1)

