def calculate_constructor_points(driver1_score: float, driver2_score: float) -> float:
    """
    A pontuação base do construtor é a soma da pontuação de seus dois pilotos.
    """
    return driver1_score + driver2_score

def calculate_pit_stop_points(rank: int) -> int:
    """
    Pontos por tempo de pit stop (Rank na corrida).
    - 1º mais rápido: +10 pts
    - 2º mais rápido: +5 pts
    - 3º mais rápido: +3 pts
    """
    points_map = {1: 10, 2: 5, 3: 3}
    return points_map.get(rank, 0)

def calculate_constructor_bonuses(double_podium: bool, double_q3: bool) -> int:
    """
    Bônus específicos para construtores.
    - Pódio Duplo (ambos Top 3): +10 pts
    - Ambos no Q3 (Qualifying): +5 pts
    """
    points = 0
    if double_podium:
        points += 10
    if double_q3:
        points += 5
    return points

def calculate_constructor_penalty(double_dnf: bool) -> int:
    """
    Penalidade se ambos os carros não terminarem (Double DNF).
    """
    if double_dnf:
        return -10
    return 0
