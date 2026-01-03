def calculate_sprint_position_points(position: int) -> int:
    """
    Calcula pontos baseados na posição final da Sprint.
    Regra padrão F1: 1º=8, 2º=7, 3º=6, 4º=5, 5º=4, 6º=3, 7º=2, 8º=1.
    """
    points_map = {
        1: 8, 2: 7, 3: 6, 4: 5,
        5: 4, 6: 3, 7: 2, 8: 1
    }
    return points_map.get(position, 0)

def calculate_sprint_overtake_points(grid_position: int, finish_position: int) -> int:
    """
    Calcula pontos por posições ganhas na Sprint.
    Regra comum: +1 ponto por posição ganha em relação ao grid.
    Se perdeu posições, o resultado será negativo (pontos negativos).
    """
    return grid_position - finish_position

def calculate_sprint_dnf_penalty() -> int:
    """
    Penalidade se não terminar a Sprint (DNF).
    """
    return -5

def calculate_sprint_fastest_lap(is_fastest: bool) -> int:
    """
    Pontos para volta mais rápida na Sprint (se aplicável na liga).
    Muitas ligas não pontuam FL na Sprint, mas deixamos parametrizado.
    """
    return 1 if is_fastest else 0
