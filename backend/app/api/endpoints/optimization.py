"""
Endpoints para otimização de times de Fantasy F1.
"""
from typing import Dict, Literal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.optimizer import TeamOptimizer


router = APIRouter()


class OptimizeRequest(BaseModel):
    """Modelo de requisição para otimização."""
    budget: float = Field(default=100.0, ge=0.0, description="Orçamento disponível em milhões")
    strategy: Literal["points", "value", "balanced"] = Field(
        default="points",
        description="Estratégia de otimização: 'points' (maximiza pontos), 'value' (maximiza sentiment), 'balanced' (equilibrado)"
    )


@router.post("/optimize")
def optimize_team(request: OptimizeRequest) -> Dict:
    """
    Otimiza um time de Fantasy F1 baseado no orçamento e estratégia fornecidos.
    
    Args:
        request: Requisição com orçamento e estratégia
    
    Returns:
        Dict com:
            - drivers: Lista de IDs dos pilotos recomendados
            - constructors: Lista de IDs dos construtores recomendados
            - total_score: Score total do time
            - total_cost: Custo total
            - budget_remaining: Orçamento restante
    
    Raises:
        HTTPException 422: Se os parâmetros forem inválidos
        HTTPException 500: Se houver erro na otimização
    """
    try:
        optimizer = TeamOptimizer()
        result = optimizer.find_best_team(
            budget=request.budget,
            strategy=request.strategy
        )
        
        return {
            "drivers": result["drivers"],
            "constructors": result["constructors"],
            "total_score": result["total_score"],
            "total_cost": result["total_cost"],
            "budget_remaining": result["budget_remaining"],
            "strategy": request.strategy
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao otimizar time: {str(e)}"
        )


