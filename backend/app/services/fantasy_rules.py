"""
Serviço para validação de regras do Fantasy F1 2025.
"""
from typing import List, Tuple, Dict, Any


def validate_team(drivers: List[str], constructors: List[str], prices_data: List[Dict[str, Any]]) -> Tuple[bool, str]:
    """
    Valida um time de Fantasy F1 seguindo as regras oficiais de 2025.
    
    Regras:
        - Deve ter exatamente 5 Pilotos
        - Deve ter exatamente 2 Construtores
        - Orçamento total <= $100.0 Milhões
        - Limite de 3 pilotos da mesma equipe
    
    Args:
        drivers: Lista de IDs dos pilotos selecionados
        constructors: Lista de IDs dos construtores selecionados
        prices_data: Lista de dicionários com dados de preços (formato f1_prices.json)
    
    Returns:
        Tuple[bool, str]: (is_valid, message)
    """
    # Cria dicionário para acesso rápido aos dados
    data_dict = {item["id"]: item for item in prices_data}
    
    # 1. Verifica número de pilotos
    if len(drivers) != 5:
        return False, f"O time deve ter exatamente 5 pilotos. Atualmente: {len(drivers)}"
    
    # 2. Verifica número de construtores
    if len(constructors) != 2:
        return False, f"O time deve ter exatamente 2 construtores. Atualmente: {len(constructors)}"
    
    # 3. Verifica se todos os IDs existem nos dados
    for driver_id in drivers:
        if driver_id not in data_dict:
            return False, f"Piloto '{driver_id}' não encontrado nos dados"
        if data_dict[driver_id]["type"] != "DRIVER":
            return False, f"'{driver_id}' não é um piloto"
    
    for constructor_id in constructors:
        if constructor_id not in data_dict:
            return False, f"Construtor '{constructor_id}' não encontrado nos dados"
        if data_dict[constructor_id]["type"] != "CONSTRUCTOR":
            return False, f"'{constructor_id}' não é um construtor"
    
    # 4. Calcula orçamento total
    total_cost = 0.0
    for driver_id in drivers:
        total_cost += data_dict[driver_id]["price"]
    for constructor_id in constructors:
        total_cost += data_dict[constructor_id]["price"]
    
    if total_cost > 100.0:
        return False, f"Orçamento estourado: ${total_cost:.2f}M (máximo: $100.0M)"
    
    # 5. Verifica limite de 3 pilotos da mesma equipe
    team_counts = {}
    for driver_id in drivers:
        team = data_dict[driver_id]["team"]
        team_counts[team] = team_counts.get(team, 0) + 1
        if team_counts[team] > 3:
            return False, f"Limite de 3 pilotos por equipe excedido. Equipe '{team}' tem {team_counts[team]} pilotos"
    
    return True, "Time válido!"


