from typing import List
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

def criar_preprocessador(numeric_features: List[str], categorical_features: List[str]) -> ColumnTransformer:
    """
    Cria um objeto ColumnTransformer para pré-processamento de dados.
    
    O pipeline inclui:
    - Numéricos: Imputação pela mediana + Padronização (StandardScaler).
    - Categóricos: Imputação de valor constante + OneHotEncoding.
    
    Args:
        numeric_features (List[str]): Lista de nomes das colunas numéricas.
        categorical_features (List[str]): Lista de nomes das colunas categóricas.
        
    Returns:
        ColumnTransformer: Objeto Scikit-learn configurado para transformar os dados.
    """
    
    # Pipeline para variáveis numéricas
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    # Pipeline para variáveis categóricas
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    # Combina os transformadores
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='drop' # Descarta colunas não listadas (pode ser ajustado para 'passthrough')
    )
        
    return preprocessor
