def calculate_transfer_penalty(transfers_made: int, free_transfers: int) -> int:
    """
    Calcula a penalidade de pontos por transferências excedentes.
    - Cada transferência acima do limite custa -10 pontos.
    - Se transfers_made <= free_transfers, penalidade é 0.
    """
    excess_transfers = transfers_made - free_transfers
    if excess_transfers > 0:
        return excess_transfers * -10
    return 0

def get_free_transfers_count(is_wildcard_active: bool, is_limitless_active: bool, saved_transfers: int) -> int:
    """
    Retorna o número de transferências gratuitas disponíveis.
    - Se Wildcard ou Limitless ativos: Infinito (retorna um número alto, ex: 999).
    - Regra padrão: 2 por semana, podendo acumular até 3 (se saved_transfers > 0).
    """
    if is_wildcard_active or is_limitless_active:
        return 999
    
    base_transfers = 2
    total_available = base_transfers + saved_transfers
    
    # Limite máximo acumulado geralmente é 3
    return min(total_available, 3)

def carry_over_transfers(transfers_made: int, available_transfers: int) -> int:
    """
    Calcula quantas transferências podem ser acumuladas para a próxima semana.
    - Se usou menos que o disponível, guarda 1 (máximo acumulado de 1 extra).
    """
    unused = available_transfers - transfers_made
    if unused > 0:
        return 1
    return 0
