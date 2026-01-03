import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from app.ml.clean_data import limpar_dados
from app.ml.feature_engineering import criar_features
from app.ml.encode_scale import criar_preprocessador
from app.core.config import settings

def treinar_modelo(df_raw: pd.DataFrame, target_col: str = 'points'):
    """
    Executa o pipeline completo de treinamento:
    1. Limpeza
    2. Feature Engineering
    3. Pré-processamento (Scaling/Encoding)
    4. Treinamento (RandomForest)
    5. Salvamento do modelo
    """
    print("Iniciando pipeline de treinamento...")
    
    # 1. Limpeza
    df_clean = limpar_dados(df_raw)
    
    # 2. Feature Engineering
    df_features = criar_features(df_clean)
    
    # Definição das features
    numeric_features = ['grid', 'position_gain']
    categorical_features = ['driverRef', 'constructorRef', 'circuitId']
    
    # Verifica se colunas existem antes de prosseguir
    # (Adiciona verificações de segurança simples)
    available_num = [c for c in numeric_features if c in df_features.columns]
    available_cat = [c for c in categorical_features if c in df_features.columns]
    
    X = df_features[available_num + available_cat]
    y = df_features[target_col] if target_col in df_features.columns else None
    
    if y is None:
        raise ValueError(f"Coluna alvo '{target_col}' não encontrada no dataset.")

    # 3. Pré-processamento
    preprocessor = criar_preprocessador(available_num, available_cat)
    
    # 4. Pipeline Final
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    print("Treinando RandomForestRegressor...")
    model_pipeline.fit(X, y)
    
    # 5. Salvar Modelo
    save_path = settings.MODEL_PATH
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    joblib.dump(model_pipeline, save_path)
    
    print(f"Modelo treinado e salvo em: {save_path}")
    return model_pipeline
