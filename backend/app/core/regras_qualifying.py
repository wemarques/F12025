def calculate_qualifying_position_points(position: int) -> int:
    """
    Calcula pontos baseados na posição final do Qualifying.
    Regra: Pole = 10pts, até 0pts para posições baixas (exemplo genérico, ajustar conforme regra oficial exata).
    """
    points_map = {
        1: 10, 2: 9, 3: 8, 4: 7, 5: 6,
        6: 5, 7: 4, 8: 3, 9: 2, 10: 1
    }
    return points_map.get(position, 0)

def calculate_qualifying_bonus(driver_teammate_comparison: bool, reached_q3: bool) -> int:
    """
    Calcula bônus de performance no Qualifying.
    - Superou companheiro: +2 pts
    - Chegou ao Q3: +1 pt
    """
    points = 0
    if driver_teammate_comparison:
        points += 2
    if reached_q3:
        points += 1
    return points

def calculate_not_classified_penalty() -> int:
    """
    Penalidade se não classificar (DSQ).
    """
    return -5
