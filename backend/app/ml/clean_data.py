import pandas as pd
import numpy as np

def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza a limpeza inicial dos dados de Fórmula 1.
    
    Ações realizadas:
    1. Substitui valores '\\N' (comuns em datasets Kaggle/Ergast) por NaN.
    2. Converte colunas numéricas que estavam como texto.
    3. Remove duplicatas.
    4. Trata valores nulos (estratégia básica).
    
    Args:
        df (pd.DataFrame): DataFrame bruto.
        
    Returns:
        pd.DataFrame: DataFrame limpo e pronto para feature engineering.
    """
    # Evita modificar o original
    df_clean = df.copy()
    
    # 1. Tratar '\N' como NaN
    df_clean.replace(r'\\N', np.nan, regex=True, inplace=True)
    
    # 2. Tentar converter colunas para numérico onde possível
    # Itera sobre colunas object para tentar conversão
    for col in df_clean.select_dtypes(include=['object']).columns:
        try:
            df_clean[col] = pd.to_numeric(df_clean[col])
        except (ValueError, TypeError):
            # Se der erro (ex: tem letras misturadas), mantém como estava
            pass
            
    # 3. Remover duplicatas
    df_clean.drop_duplicates(inplace=True)
    
    # 4. Tratamento básico de nulos (pode ser ajustado conforme a coluna)
    # Exemplo: Preencher tempos nulos com 0 ou média, mas aqui vamos apenas
    # garantir que não quebre o pipeline.
    # Para ML, geralmente tratamos nulos no Pipeline (SimpleImputer), 
    # então aqui focamos mais em limpeza estrutural.
    
    return df_clean
