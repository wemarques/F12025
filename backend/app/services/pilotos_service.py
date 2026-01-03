from typing import List, Dict

def listar_pilotos() -> List[Dict]:
    """
    Retorna a lista de pilotos da temporada 2025.
    """
    return [
        {"id": 1, "name": "Max Verstappen", "team": "Red Bull Racing", "number": 1},
        {"id": 2, "name": "Sergio Perez", "team": "Red Bull Racing", "number": 11},
        {"id": 3, "name": "Lewis Hamilton", "team": "Ferrari", "number": 44},
        {"id": 4, "name": "Charles Leclerc", "team": "Ferrari", "number": 16},
        {"id": 5, "name": "Lando Norris", "team": "McLaren", "number": 4},
        {"id": 6, "name": "Oscar Piastri", "team": "McLaren", "number": 81},
        {"id": 7, "name": "George Russell", "team": "Mercedes", "number": 63},
        {"id": 8, "name": "Kimi Antonelli", "team": "Mercedes", "number": 12},
    ]
