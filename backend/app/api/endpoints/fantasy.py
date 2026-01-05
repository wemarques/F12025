"""
Endpoint para otimização de time de Fantasy F1.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from app.services.fantasy_optimizer import find_best_team

router = APIRouter()


class OptimizationRequest(BaseModel):
    budget: float = 100.0
    custom_points_projections: Optional[Dict[str, float]] = None


@router.post("/optimize")
async def optimize_team(request: OptimizationRequest):
    """
    Otimiza um time de Fantasy F1 maximizando expected_points.
    
    Args:
        request: OptimizationRequest com budget (padrão: 100.0)
    
    Returns:
        Dict com a melhor equipe:
        {
            "drivers": [list of driver IDs],
            "constructors": [list of constructor IDs],
            "total_points": float,
            "total_cost": float,
            "budget_remaining": float
        }
    """
    try:
        if request.budget <= 0:
            raise HTTPException(status_code=400, detail="Orçamento deve ser maior que zero")
        
        result = find_best_team(request.budget, request.custom_points_projections)
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Arquivo de dados não encontrado: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao otimizar time: {str(e)}")

