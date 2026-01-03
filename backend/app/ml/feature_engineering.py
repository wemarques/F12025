import pandas as pd
import numpy as np

def criar_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gera novas features a partir dos dados limpos.
    
    Features criadas (se colunas disponíveis):
    - position_gain: Ganho de posições (Grid - Posição Final)
    - podium_finish: Booleano se terminou no pódio (Top 3)
    - in_points: Booleano se terminou na zona de pontuação (Top 10)
    - front_row: Largou na primeira fila (Grid <= 2)
    
    Args:
        df (pd.DataFrame): DataFrame contendo colunas como 'grid', 'positionOrder', etc.
        
    Returns:
        pd.DataFrame: DataFrame enriquecido com novas colunas.
    """
    df_feat = df.copy()
    
    # 1. Ganho de posições (Grid vs Resultado)
    # Quanto maior, mais posições ganhou. Negativo significa que perdeu posições.
    if 'grid' in df_feat.columns and 'positionOrder' in df_feat.columns:
        df_feat['position_gain'] = df_feat['grid'] - df_feat['positionOrder']
        
    # 2. Indicadores de performance
    if 'positionOrder' in df_feat.columns:
        # Terminou no pódio?
        df_feat['podium_finish'] = df_feat['positionOrder'].apply(lambda x: 1 if x <= 3 else 0)
        # Terminou nos pontos? (Regra atual Top 10)
        df_feat['in_points'] = df_feat['positionOrder'].apply(lambda x: 1 if x <= 10 else 0)
        
    # 3. Indicadores de Grid
    if 'grid' in df_feat.columns:
        # Largou na primeira fila?
        df_feat['front_row'] = df_feat['grid'].apply(lambda x: 1 if x <= 2 else 0)
        # Pole Position?
        df_feat['pole_position'] = df_feat['grid'].apply(lambda x: 1 if x == 1 else 0)

    return df_feat
