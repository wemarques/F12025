"""
Módulo de simulação de clima para corridas F1.
"""
import random
from enum import Enum


class WeatherCondition(Enum):
    """Condições climáticas possíveis."""
    DRY = "DRY"
    MIXED = "MIXED"
    WET = "WET"


class WeatherEngine:
    """Motor de simulação de impacto climático."""
    
    @staticmethod
    def apply_weather_impact(
        lap_time: float,
        condition: WeatherCondition,
        driver_skill: float = 1.0
    ) -> float:
        """
        Aplica o impacto do clima no tempo de volta.
        
        Args:
            lap_time: Tempo de volta base (em segundos)
            condition: Condição climática (DRY, MIXED, WET)
            driver_skill: Fator de habilidade do piloto (1.0 = padrão, >1.0 = melhor na chuva)
        
        Returns:
            Tempo de volta ajustado pelo clima (em segundos)
        """
        if condition == WeatherCondition.DRY:
            # Condições secas: sem alteração
            return lap_time
        
        elif condition == WeatherCondition.WET:
            # Condições molhadas: aumenta tempo em 15% a 20% (randomizado)
            # Aumenta a variabilidade (simulado com multiplicador maior)
            rain_multiplier = random.uniform(1.15, 1.20)
            # Pilotos com mais habilidade na chuva sofrem menos penalidade
            adjusted_multiplier = 1.0 + (rain_multiplier - 1.0) / driver_skill
            return lap_time * adjusted_multiplier
        
        elif condition == WeatherCondition.MIXED:
            # Condições mistas: aumenta tempo em 5% a 10%
            # Alta variabilidade (simula Safety Car e condições variáveis)
            mixed_multiplier = random.uniform(1.05, 1.10)
            adjusted_multiplier = 1.0 + (mixed_multiplier - 1.0) / driver_skill
            return lap_time * adjusted_multiplier
        
        # Fallback (não deveria acontecer)
        return lap_time
    
    @staticmethod
    def determine_weather(rain_probability: float) -> WeatherCondition:
        """
        Determina a condição climática baseado na probabilidade de chuva.
        
        Args:
            rain_probability: Probabilidade de chuva (0.0 a 1.0, onde 1.0 = chuva garantida)
        
        Returns:
            WeatherCondition determinada
        """
        if rain_probability <= 0.0:
            return WeatherCondition.DRY
        
        if rain_probability >= 1.0:
            return WeatherCondition.WET
        
        # Gera um número aleatório entre 0 e 1
        random_value = random.random()
        
        if random_value <= rain_probability:
            # Chuva determinada
            # Se a probabilidade for alta (>0.7), é mais provável ser WET puro
            # Se for média (0.3-0.7), pode ser MIXED
            # Se for baixa (<0.3), mais provável MIXED
            if rain_probability > 0.7:
                return WeatherCondition.WET
            elif rain_probability > 0.3:
                # 60% WET, 40% MIXED
                return WeatherCondition.WET if random.random() < 0.6 else WeatherCondition.MIXED
            else:
                # Mais provável MIXED para probabilidades baixas
                return WeatherCondition.MIXED if random.random() < 0.7 else WeatherCondition.WET
        
        # Sem chuva
        return WeatherCondition.DRY

