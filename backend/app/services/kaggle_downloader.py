import os
from kaggle.api.kaggle_api_extended import KaggleApi
from app.core.config import settings

def baixar_dataset_f1():
    """
    Autentica na API do Kaggle e baixa o dataset 'rohanrao/formula-1-world-championship-1950-2020'
    para o diretório de dados raw configurado.
    """
    try:
        api = KaggleApi()
        api.authenticate()
        
        dataset = "rohanrao/formula-1-world-championship-1950-2020"
        target_path = os.path.join(settings.DATA_DIR, "raw")
        
        if not os.path.exists(target_path):
            os.makedirs(target_path)
            
        print(f"Iniciando download do dataset {dataset} para {target_path}...")
        
        api.dataset_download_files(dataset, path=target_path, unzip=True)
        
        print("Download e extração concluídos com sucesso.")
        return True
        
    except Exception as e:
        print(f"Erro ao baixar dataset do Kaggle: {str(e)}")
        return False
