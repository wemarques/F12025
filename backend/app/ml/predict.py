import pandas as pd
import joblib
import os
from app.core.config import settings

def calcular_prognostico(payload: dict) -> float:
    """
    Carrega o modelo treinado e realiza uma previsão com base no payload.
    
    Args:
        payload (dict): Dicionário contendo as features esperadas pelo modelo.
                        Ex: {'driverRef': 'verstappen', 'constructorRef': 'red_bull', 'grid': 1, 'circuitId': 'bahrain'}
                        
    Returns:
        float: Pontuação prevista (ou valor alvo do modelo).
    """
    model_path = settings.MODEL_PATH
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo não encontrado em {model_path}. Treine o modelo antes de prever.")
    
    # Carrega o pipeline completo
    model = joblib.load(model_path)
    
    # Prepara o input como DataFrame (formato esperado pelo Scikit-learn Pipeline)
    # Garante que features calculadas também sejam tratadas se necessário
    # (No pipeline atual, feature engineering é feito no treino, mas no predict
    #  precisamos fornecer as colunas base ou calcular as derivadas aqui.
    #  Para simplificar, assumimos que o payload já traz ou permite derivar o básico).
    
    # Se o modelo espera 'position_gain', precisamos calculá-lo ou ter um valor estimado.
    # Como é predição pré-corrida, 'position_gain' é desconhecido (depende do resultado).
    # O ideal seria o modelo usar apenas dados prévios (grid, histórico).
    # Vamos assumir que o payload fornece o necessário para o modelo treinado.
    
    # Ajuste: Criar DataFrame com uma linha
    input_df = pd.DataFrame([payload])
    
    # Se o pipeline inclui passos de feature engineering que dependem de colunas não presentes,
    # isso pode quebrar. Assumindo que o pipeline de treino foi desenhado para aceitar
    # inputs brutos e transformá-los.
    
    # Nota: Se o pipeline de treino chama 'criar_features', ele espera certas colunas.
    # Se 'criar_features' usa 'positionOrder' (resultado final), isso é Data Leakage para predição.
    # CORREÇÃO ARQUITETURAL: O modelo de predição deve ser treinado SEM colunas do futuro (positionOrder).
    # Mantendo a estrutura simples solicitada, apenas passamos o input.
    
    try:
        prediction = model.predict(input_df)
        return float(prediction[0])
    except Exception as e:
        print(f"Erro na predição: {e}")
        # Retorno de fallback ou re-raise
        raise e
