from fastapi import APIRouter
from backend.models.prediction_request import PredictionRequest
from backend.services.model_service import predict_points

router = APIRouter()

@router.post("/")
def predict(request: PredictionRequest):
    result = predict_points(request)
    return {"prediction": result}
