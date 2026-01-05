def predict_points(request):
    """
    Função placeholder.
    Depois você substitui pelo modelo real.
    """
    base = 25
    quali_bonus = max(0, 10 - request.quali_position)
    race_bonus = max(0, 10 - request.race_position)

    return base + quali_bonus + race_bonus
