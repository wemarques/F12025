"""
Serviço para carregar dados de Fantasy F1 (Pilotos e Construtores).
"""
import json
import os
import pandas as pd
from pathlib import Path
from typing import Tuple


def get_data_path() -> Path:
    """
    Retorna o caminho do arquivo de dados.
    
    Returns:
        Path: Caminho para o arquivo f1_2025_start.json
    """
    # Caminho relativo: backend/data/f1_2025_start.json
    backend_dir = Path(__file__).parent.parent.parent
    data_file = backend_dir / "data" / "f1_2025_start.json"
    return data_file


def load_assets() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Carrega os ativos (Pilotos e Construtores) do arquivo JSON.
    
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: 
            - Primeiro DataFrame: Pilotos (type == "DRIVER")
            - Segundo DataFrame: Construtores (type == "CONSTRUCTOR")
    
    Raises:
        FileNotFoundError: Se o arquivo de dados não for encontrado.
        json.JSONDecodeError: Se o arquivo JSON estiver malformado.
    """
    data_file = get_data_path()
    
    if not data_file.exists():
        raise FileNotFoundError(
            f"Arquivo de dados não encontrado: {data_file}\n"
            f"Certifique-se de que o arquivo f1_2025_start.json existe no diretório backend/data/"
        )
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Converte para DataFrame
    df_all = pd.DataFrame(data)
    
    # Separa em Drivers e Constructors
    df_drivers = df_all[df_all['type'] == 'DRIVER'].copy()
    df_constructors = df_all[df_all['type'] == 'CONSTRUCTOR'].copy()
    
    # Ordena por preço (maior primeiro) e depois por nome
    df_drivers = df_drivers.sort_values(['price', 'name'], ascending=[False, True]).reset_index(drop=True)
    df_constructors = df_constructors.sort_values(['price', 'name'], ascending=[False, True]).reset_index(drop=True)
    
    return df_drivers, df_constructors


def get_driver_by_id(driver_id: str) -> pd.Series:
    """
    Obtém um piloto pelo ID.
    
    Args:
        driver_id: ID do piloto (ex: "VER", "NOR")
    
    Returns:
        pd.Series: Dados do piloto
    
    Raises:
        ValueError: Se o piloto não for encontrado.
    """
    df_drivers, _ = load_assets()
    driver = df_drivers[df_drivers['id'] == driver_id]
    
    if driver.empty:
        raise ValueError(f"Piloto '{driver_id}' não encontrado")
    
    return driver.iloc[0]


def get_constructor_by_id(constructor_id: str) -> pd.Series:
    """
    Obtém um construtor pelo ID.
    
    Args:
        constructor_id: ID do construtor (ex: "RBR", "MCL")
    
    Returns:
        pd.Series: Dados do construtor
    
    Raises:
        ValueError: Se o construtor não for encontrado.
    """
    _, df_constructors = load_assets()
    constructor = df_constructors[df_constructors['id'] == constructor_id]
    
    if constructor.empty:
        raise ValueError(f"Construtor '{constructor_id}' não encontrado")
    
    return constructor.iloc[0]

