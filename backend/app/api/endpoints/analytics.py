"""
Endpoints para análise de telemetria e comparação de voltas.
"""
from typing import Dict, Literal
from fastapi import APIRouter, HTTPException, Query

from app.services.fastf1_adapter import get_session_data


router = APIRouter()


@router.get("/compare-laps")
def compare_laps(
    year: int = Query(..., description="Ano da temporada (ex: 2025)"),
    gp: str = Query(..., description="Nome do Grande Prêmio (ex: 'Bahrain', 'Monaco')"),
    session_type: Literal["FP1", "FP2", "FP3", "Q", "S", "SS", "R"] = Query(
        default="R", description="Tipo de sessão"
    ),
    driver1: str = Query(..., description="Código do primeiro piloto (ex: 'VER', 'HAM')"),
    driver2: str = Query(..., description="Código do segundo piloto (ex: 'VER', 'HAM')")
) -> Dict:
    """
    Compara as voltas mais rápidas de dois pilotos em uma sessão.
    
    Retorna dados de telemetria (distância e velocidade) para comparação visual
    entre as voltas mais rápidas de cada piloto.
    
    Args:
        year: Ano da temporada.
        gp: Nome do Grande Prêmio.
        session_type: Tipo de sessão (FP1, FP2, FP3, Q, S, SS, R).
        driver1: Código do primeiro piloto (3 letras, ex: 'VER').
        driver2: Código do segundo piloto (3 letras, ex: 'HAM').
    
    Returns:
        Dicionário com dados de telemetria de ambos os pilotos:
        {
            "driver1": {
                "driver": "VER",
                "lapTime": "1:28.123",
                "distance": [0.0, 10.5, ...],
                "speed": [120.5, 125.3, ...]
            },
            "driver2": {
                "driver": "HAM",
                "lapTime": "1:28.456",
                "distance": [0.0, 10.3, ...],
                "speed": [119.8, 124.9, ...]
            }
        }
    
    Raises:
        HTTPException 404: Se um dos pilotos não for encontrado ou não tiver voltas válidas.
        HTTPException 503: Se houver erro ao carregar dados da sessão (tratado pelo adapter).
    """
    # Carrega a sessão (já trata erros 503/422)
    session = get_session_data(year, gp, session_type)
    
    # Obtém voltas sem pit stops
    laps = session.laps.pick_wo_box()
    
    # Helper para processar piloto
    def get_driver_fastest_lap(driver_code: str) -> Dict:
        """Obtém a volta mais rápida de um piloto e retorna dados de telemetria."""
        try:
            # Filtra voltas do piloto
            driver_laps = laps.pick_drivers(driver_code)
            
            if driver_laps.empty:
                raise HTTPException(
                    status_code=404,
                    detail=f"Piloto '{driver_code}' não encontrado na sessão {year} {gp} {session_type}"
                )
            
            # Obtém a volta mais rápida (retorna Lap ou None)
            fastest_lap = driver_laps.pick_fastest()
            
            if fastest_lap is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Piloto '{driver_code}' não possui voltas válidas na sessão {year} {gp} {session_type}"
                )
            
            # Obtém telemetria do carro e adiciona distância
            car_data = fastest_lap.get_car_data().add_distance()
            
            # Extrai arrays de distância e velocidade
            distance = car_data["Distance"].tolist()
            speed = car_data["Speed"].tolist()
            
            # Obtém o tempo da volta (Lap é uma Series, acessa diretamente)
            lap_time = str(fastest_lap["LapTime"])
            
            return {
                "driver": driver_code,
                "lapTime": lap_time,
                "distance": distance,
                "speed": speed
            }
            
        except HTTPException:
            # Re-raise HTTPExceptions
            raise
        except Exception as e:
            # Outros erros (ex: problema ao processar telemetria)
            raise HTTPException(
                status_code=404,
                detail=f"Erro ao processar dados do piloto '{driver_code}': {str(e)}"
            )
    
    # Processa ambos os pilotos
    try:
        driver1_data = get_driver_fastest_lap(driver1)
        driver2_data = get_driver_fastest_lap(driver2)
        
        return {
            "driver1": driver1_data,
            "driver2": driver2_data
        }
    except HTTPException:
        # Re-raise HTTPExceptions
        raise

