from typing import List, Dict, Union

def apply_autopilot(team_scores: Dict[str, float]) -> str:
    """
    Piloto Automático: Identifica o piloto com maior pontuação no time
    para receber o bônus de DRS (se não foi atribuído corretamente).
    Retorna o ID do piloto que deve receber o bônus.
    """
    pass

def apply_extra_drs(score: float) -> float:
    """
    Extra DRS: Triplica a pontuação do piloto escolhido (3x),
    em vez do padrão (2x).
    """
    pass

def apply_no_negative(score: float) -> float:
    """
    Sem Negativo: Se a pontuação total (ou parcial) for negativa,
    ela é ajustada para 0.
    """
    pass

def validate_wildcard_usage(is_active: bool) -> bool:
    """
    Coringa (Wildcard): Permite transferências ilimitadas sem penalidade
    de pontos na rodada ativa. Retorna True se as transferências são gratuitas.
    """
    pass

def get_limitless_budget(is_active: bool, standard_budget: float) -> float:
    """
    Limitless: Permite montar um time sem teto orçamentário.
    Se ativo, retorna um valor de orçamento 'infinito' ou muito alto.
    Caso contrário, retorna o orçamento padrão.
    """
    pass

def apply_final_fix(current_lineup: List[str], driver_out: str, driver_in: str) -> List[str]:
    """
    Ajuste Final: Permite realizar uma substituição no time entre
    o Qualifying e a Corrida, mantendo os pontos já adquiridos pelo piloto removido?
    (Depende da regra específica, geralmente troca o piloto para a corrida).
    """
    pass
