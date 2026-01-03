from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.ml.regressor import regressor

router = APIRouter()

class PredictionRequest(BaseModel):
    driver: str
    constructor: str
    grid: int

class PredictionResponse(BaseModel):
    driver: str
    predicted_points: float

@router.post("/predict", response_model=PredictionResponse)
def predict_points(request: PredictionRequest):
    """
    Gera um prognóstico de pontos para um piloto em uma corrida específica.
    """
    try:
        points = regressor.predict(
            driver=request.driver,
            constructor=request.constructor,
            grid=request.grid
        )
        
        return PredictionResponse(
            driver=request.driver,
            predicted_points=points
        )
    except ValueError as ve:
        # Geralmente lançado se o modelo não estiver treinado
        raise HTTPException(status_code=503, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao gerar prognóstico: {str(e)}")
