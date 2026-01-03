from typing import List, Dict
from datetime import datetime

def get_all_races() -> List[Dict]:
    """
    Retorna a lista de corridas da temporada 2025 (Mock).
    """
    return [
        {"round": 1, "name": "Australian Grand Prix", "circuit": "Albert Park Circuit", "date": "2025-03-16"},
        {"round": 2, "name": "Chinese Grand Prix", "circuit": "Shanghai International Circuit", "date": "2025-03-23"},
        {"round": 3, "name": "Japanese Grand Prix", "circuit": "Suzuka International Racing Course", "date": "2025-04-06"},
        {"round": 4, "name": "Bahrain Grand Prix", "circuit": "Bahrain International Circuit", "date": "2025-04-13"},
        {"round": 5, "name": "Saudi Arabian Grand Prix", "circuit": "Jeddah Corniche Circuit", "date": "2025-04-20"},
        {"round": 6, "name": "Miami Grand Prix", "circuit": "Miami International Autodrome", "date": "2025-05-04"},
        # Adicionar mais corridas conforme necessário
    ]

def get_race_by_round(round_number: int) -> Dict:
    races = get_all_races()
    for race in races:
        if race["round"] == round_number:
            return race
    return None

def proxima_corrida() -> Dict:
    """
    Retorna a próxima corrida agendada (fictícia/mock).
    Considerando a data atual simulada ou retornando a primeira da lista.
    """
    # Lógica simples: retorna a primeira corrida que ainda não aconteceu
    # Como é um mock e estamos em '2026' no ambiente, mas os dados são '2025',
    # vamos retornar a primeira corrida da lista como exemplo.
    
    races = get_all_races()
    # Exemplo estático retornando a corrida da Austrália
    return races[0]
