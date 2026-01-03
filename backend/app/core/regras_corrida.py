def calculate_race_position_points(position: int) -> int:
    """
    Calcula pontos baseados na posição final da Corrida (Feature Race).
    Regra padrão F1: 25, 18, 15, 12, 10, 8, 6, 4, 2, 1.
    """
    points_map = {
        1: 25, 2: 18, 3: 15, 4: 12, 5: 10,
        6: 8, 7: 6, 8: 4, 9: 2, 10: 1
    }
    return points_map.get(position, 0)

def calculate_race_overtake_points(grid_position: int, finish_position: int) -> int:
    """
    Calcula pontos por posições ganhas na Corrida.
    Regra comum: +1 ponto por posição ganha (max 10), -1 por posição perdida (max -10).
    Muitas ligas limitam a 5 ou 10 pontos de ultrapassagem. Aqui deixamos ilimitado por padrão.
    """
    diff = grid_position - finish_position
    return diff

def calculate_race_bonuses(fastest_lap: bool, driver_of_the_day: bool, beat_teammate: bool) -> int:
    """
    Calcula bônus diversos de performance na corrida.
    - Volta mais rápida: +5 pts (Fantasy costuma dar mais que a F1 real)
    - Piloto do dia: +5 pts
    - Superou companheiro: +3 pts
    """
    points = 0
    if fastest_lap:
        points += 5
    if driver_of_the_day:
        points += 5
    if beat_teammate:
        points += 3
    return points

def calculate_completion_points(status: str) -> int:
    """
    Pontos baseados no status de término.
    - Terminou (Finished / +1 Lap): +1 pt
    - DNF (Did Not Finish): -10 pts
    - DSQ (Disqualified): -20 pts
    """
    status_lower = status.lower()
    
    # Lista de status considerados como "Terminou"
    finished_statuses = ['finished', '+1 lap', '+2 laps', '+3 laps', '+4 laps', '+5 laps']
    
    if any(s in status_lower for s in finished_statuses):
        return 1
    elif 'disqualified' in status_lower or 'dsq' in status_lower:
        return -20
    else:
        # Assume DNF para outros status (Collision, Engine, etc) se não classificou
        return -10
