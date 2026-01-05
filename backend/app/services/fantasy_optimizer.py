"""
Serviço de otimização para encontrar o melhor time de Fantasy F1 usando f1_prices.json.
"""
import itertools
import json
from pathlib import Path
from typing import Dict, List, Tuple


def load_prices_data() -> List[Dict]:
    """Carrega dados de preços do arquivo f1_prices.json"""
    backend_dir = Path(__file__).parent.parent.parent
    prices_file = backend_dir / "data" / "f1_prices.json"
    
    if not prices_file.exists():
        raise FileNotFoundError(f"Arquivo {prices_file} não encontrado")
    
    with open(prices_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_best_team(budget: float = 100.0, custom_points_projections: Dict[str, float] = None) -> Dict:
    """
    Encontra o melhor time de Fantasy F1 maximizando expected_points.
    
    Algoritmo:
        1. Separa Pilotos e Construtores
        2. Gera todas as combinações possíveis de 2 Construtores
        3. Para cada par de construtores, calcula o orçamento restante
        4. Gera combinações de 5 Pilotos que caibam nesse restante
        5. Respeita a regra: Máximo 3 pilotos da mesma equipe
        6. Maximiza a soma de expected_points
    
    Args:
        budget: Orçamento disponível (padrão: 100.0)
        custom_points_projections: Dict opcional com projeções customizadas de pontos.
            Se fornecido, usa esses valores ao invés dos valores padrão do JSON.
            Formato: {"driver_name": points, ...}
    
    Returns:
        Dict com:
        {
            "drivers": [list of driver IDs],
            "constructors": [list of constructor IDs],
            "total_points": float,
            "total_cost": float,
            "budget_remaining": float
        }
    """
    prices_data = load_prices_data()
    
    # Separa pilotos e construtores
    drivers = [item for item in prices_data if item["type"] == "DRIVER"]
    constructors = [item for item in prices_data if item["type"] == "CONSTRUCTOR"]
    
    # Cria dicionário para acesso rápido
    data_dict = {item["id"]: item for item in prices_data}
    
    # Atualiza expected_points se custom_points_projections for fornecido
    if custom_points_projections:
        for item in prices_data:
            # Tenta encontrar pelo nome (chave do dict)
            if item["name"] in custom_points_projections:
                item["expected_points"] = custom_points_projections[item["name"]]
            # Também tenta encontrar pelo ID (caso o dict use IDs)
            elif item["id"] in custom_points_projections:
                item["expected_points"] = custom_points_projections[item["id"]]
    
    best_team = None
    best_points = -1.0
    
    # Gera todas as combinações de 2 construtores
    constructor_combinations = list(itertools.combinations([c["id"] for c in constructors], 2))
    
    for constructor_pair in constructor_combinations:
        # Calcula custo dos construtores
        constructor_cost = sum(data_dict[cid]["price"] for cid in constructor_pair)
        remaining_budget = budget - constructor_cost
        
        # Se não sobra orçamento suficiente, pula
        if remaining_budget < 0:
            continue
        
        # Gera combinações de 5 pilotos
        driver_combinations = list(itertools.combinations([d["id"] for d in drivers], 5))
        
        for driver_combo in driver_combinations:
            # Calcula custo dos pilotos
            driver_cost = sum(data_dict[did]["price"] for did in driver_combo)
            total_cost = constructor_cost + driver_cost
            
            # Verifica orçamento
            if total_cost > budget:
                continue
            
            # Verifica regra: máximo 3 pilotos da mesma equipe
            team_counts = {}
            for driver_id in driver_combo:
                team = data_dict[driver_id]["team"]
                team_counts[team] = team_counts.get(team, 0) + 1
                if team_counts[team] > 3:
                    break
            else:
                # Se chegou aqui, a regra foi respeitada
                # Calcula pontos totais
                driver_points = sum(data_dict[did]["expected_points"] for did in driver_combo)
                constructor_points = sum(data_dict[cid]["expected_points"] for cid in constructor_pair)
                total_points = driver_points + constructor_points
                
                # Atualiza melhor time se necessário
                if total_points > best_points:
                    best_points = total_points
                    best_team = {
                        "drivers": list(driver_combo),
                        "constructors": list(constructor_pair),
                        "total_points": total_points,
                        "total_cost": total_cost,
                        "budget_remaining": budget - total_cost
                    }
    
    if best_team is None:
        raise ValueError("Não foi possível encontrar um time válido com o orçamento disponível")
    
    return best_team

