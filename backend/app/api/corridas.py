from fastapi import APIRouter, HTTPException
from app.services import corridas_service
from typing import List, Dict

router = APIRouter()

@router.get("/", response_model=List[Dict])
def get_races():
    """
    Lista todas as corridas da temporada.
    """
    return corridas_service.get_all_races()

@router.get("/{round_number}", response_model=Dict)
def get_race(round_number: int):
    """
    Obtém detalhes de uma corrida específica pelo número da rodada.
    """
    race = corridas_service.get_race_by_round(round_number)
    if not race:
        raise HTTPException(status_code=404, detail="Corrida não encontrada")
    return race
