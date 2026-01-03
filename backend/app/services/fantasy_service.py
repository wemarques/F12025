from typing import List, Dict, Optional
from app.core import (
    regras_qualifying,
    regras_corrida,
    regras_sprint,
    regras_construtores,
    curingas,
    transferencias
)

def calculate_driver_weekend_score(driver_result: Dict) -> float:
    """
    Calcula a pontuação de um piloto individual para um fim de semana completo.
    
    Args:
        driver_result (Dict): Dados de performance do piloto (Quali, Sprint, Race).
    """
    score = 0.0
    
    # 1. Qualifying
    q_data = driver_result.get('qualifying', {})
    if q_data:
        score += regras_qualifying.calculate_qualifying_position_points(q_data.get('position', 20))
        score += regras_qualifying.calculate_qualifying_bonus(
            q_data.get('beat_teammate', False),
            q_data.get('reached_q3', False)
        )
        if not q_data.get('classified', True):
            score += regras_qualifying.calculate_not_classified_penalty()

    # 2. Sprint (se houver)
    s_data = driver_result.get('sprint', {})
    if s_data:
        score += regras_sprint.calculate_sprint_position_points(s_data.get('position', 20))
        score += regras_sprint.calculate_sprint_overtake_points(
            s_data.get('grid', 20),
            s_data.get('position', 20)
        )
        if s_data.get('dnf', False):
            score += regras_sprint.calculate_sprint_dnf_penalty()
        score += regras_sprint.calculate_sprint_fastest_lap(s_data.get('fastest_lap', False))

    # 3. Feature Race
    r_data = driver_result.get('race', {})
    if r_data:
        score += regras_corrida.calculate_race_position_points(r_data.get('position', 20))
        score += regras_corrida.calculate_race_overtake_points(
            r_data.get('grid', 20),
            r_data.get('position', 20)
        )
        score += regras_corrida.calculate_race_bonuses(
            r_data.get('fastest_lap', False),
            r_data.get('driver_of_the_day', False),
            r_data.get('beat_teammate', False)
        )
        score += regras_corrida.calculate_completion_points(r_data.get('status', 'Finished'))
        
    return score

def calculate_team_score(team: Dict, weekend_results: Dict) -> float:
    """
    Calcula a pontuação total de um time.
    
    Args:
        team (Dict): Configuração do time (pilotos, construtor, chips, DRS).
                     Ex: {
                        'drivers': [{'id': 1, 'is_drs': True}, ...],
                        'constructor_id': 10,
                        'chips': {'autopilot': False, 'no_negative': False, 'extra_drs': False},
                        'transfers_made': 0,
                        'available_transfers': 2
                     }
        weekend_results (Dict): Resultados reais do fim de semana mapeados por ID.
    """
    total_score = 0.0
    driver_scores = {}
    
    # 1. Calcular pontuação base de cada piloto
    for driver_conf in team.get('drivers', []):
        d_id = driver_conf['id']
        result = weekend_results.get('drivers', {}).get(d_id, {})
        base_score = calculate_driver_weekend_score(result)
        driver_scores[d_id] = base_score

    # 2. Aplicação de Chips e Modificadores
    chips = team.get('chips', {})
    
    # Autopilot: Muda o DRS para o melhor piloto se ativo
    drs_driver_id = None
    if chips.get('autopilot'):
        # Encontra piloto com maior pontuação
        drs_driver_id = max(driver_scores, key=driver_scores.get)
    else:
        # Busca quem está marcado com DRS no time
        for d in team.get('drivers', []):
            if d.get('is_drs'):
                drs_driver_id = d['id']
                break
    
    # Extra DRS: 3x score
    extra_drs_active = chips.get('extra_drs', False)
    
    # Somar pontuação dos pilotos com multiplicadores
    constructor_drivers_score = 0.0 # Soma para o construtor
    
    for d_id, score in driver_scores.items():
        multiplier = 1
        
        # Verifica se é o piloto DRS
        if d_id == drs_driver_id:
            multiplier = 3 if extra_drs_active else 2
            
        final_driver_score = score * multiplier
        total_score += final_driver_score
        
        # Para construtores, geralmente usa-se o score base (sem multiplicador de DRS pessoal)
        # Ou regra específica da liga. Assumiremos score base.
        constructor_drivers_score += score

    # 3. Pontuação do Construtor
    c_id = team.get('constructor_id')
    c_result = weekend_results.get('constructors', {}).get(c_id, {})
    
    # Pontos base (soma dos pilotos) + Bônus de equipe
    c_score = regras_construtores.calculate_constructor_points(
        constructor_drivers_score, 0 # Simplificação: assumindo soma já feita ou passando pilotos separados
    )
    # Na verdade, a função calculate_constructor_points pede driver1 e driver2.
    # Vamos simplificar e somar os pontos dos pilotos + bônus específicos do construtor
    c_score = constructor_drivers_score # Base
    
    c_score += regras_construtores.calculate_pit_stop_points(c_result.get('pit_rank', 99))
    c_score += regras_construtores.calculate_constructor_bonuses(
        c_result.get('double_podium', False),
        c_result.get('double_q3', False)
    )
    c_score += regras_construtores.calculate_constructor_penalty(
        c_result.get('double_dnf', False)
    )
    
    total_score += c_score

    # 4. Penalidade de Transferências (exceto se Wildcard/Limitless ativo)
    wildcard = chips.get('wildcard', False)
    limitless = chips.get('limitless', False)
    
    if not (wildcard or limitless):
        transfers_made = team.get('transfers_made', 0)
        free_transfers = team.get('available_transfers', 2)
        penalty = transferencias.calculate_transfer_penalty(transfers_made, free_transfers)
        total_score += penalty # Penalty é negativo

    # 5. Chip No Negative
    if chips.get('no_negative') and total_score < 0:
        total_score = 0.0

    return total_score

def validate_team_budget(team_ids: List[int], budget: float) -> bool:
    """
    Verifica se o custo total dos pilotos está dentro do orçamento.
    """
    total_cost = 0.0
    for d_id in team_ids:
        total_cost += get_driver_price(d_id)
    
    return total_cost <= budget

def get_driver_price(driver_id: int) -> float:
    """
    Retorna o preço atual de um piloto (Mock).
    """
    # Exemplo simples de precificação
    prices = {
        1: 30.0, # Verstappen
        2: 25.0, # Norris
        3: 20.0, # Hamilton
        4: 22.0, # Leclerc
        # Default
    }
    return prices.get(driver_id, 10.0)

def optimize_team(budget: float) -> Dict:
    """
    Gera uma sugestão de time (Mock).
    """
    return {
        "drivers": [1, 2, 5, 7, 8],
        "constructor": 1,
        "total_cost": 95.0,
        "projected_points": 150
    }
