from fastapi import APIRouter, HTTPException
from app.services import pilotos_service

router = APIRouter()

@router.get("/", response_model=list)
def get_pilotos():
    """
    Lista todos os pilotos disponíveis.
    """
    try:
        pilotos = pilotos_service.listar_pilotos()
        return pilotos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
