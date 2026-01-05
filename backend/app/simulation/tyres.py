"""
Módulo de simulação de pneus para corridas F1.
"""
from enum import Enum
from typing import Dict


class TyreCompound(Enum):
    """Compostos de pneu disponíveis."""
    SOFT = "SOFT"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    INTER = "INTER"  # Intermediate (chuva leve)
    WET = "WET"      # Wet (chuva pesada)


class TyreModel:
    """Modelo de comportamento dos pneus."""
    
    # Atributos por composto: (speed_bonus em segundos, degradation_rate em segundos/volta)
    TYRE_PROPERTIES: Dict[TyreCompound, Dict[str, float]] = {
        TyreCompound.SOFT: {
            "speed_bonus": -1.0,      # 1 segundo mais rápido que HARD
            "degradation_rate": 0.15,  # Degrada 0.15s por volta
            "max_laps": 20            # Durabilidade máxima aproximada
        },
        TyreCompound.MEDIUM: {
            "speed_bonus": -0.5,      # 0.5 segundos mais rápido que HARD
            "degradation_rate": 0.10,  # Degrada 0.10s por volta
            "max_laps": 30
        },
        TyreCompound.HARD: {
            "speed_bonus": 0.0,       # Pneu base (sem bônus)
            "degradation_rate": 0.05,  # Degrada 0.05s por volta
            "max_laps": 50
        },
        TyreCompound.INTER: {
            "speed_bonus": 0.0,       # Sem bônus em condições secas
            "degradation_rate": 0.08,  # Degrada 0.08s por volta
            "max_laps": 35
        },
        TyreCompound.WET: {
            "speed_bonus": 0.0,       # Sem bônus em condições secas
            "degradation_rate": 0.06,  # Degrada 0.06s por volta
            "max_laps": 40
        }
    }
    
    @staticmethod
    def get_lap_penalty(compound: TyreCompound, laps_used: int) -> float:
        """
        Calcula a penalidade de tempo (em segundos) devido ao desgaste do pneu.
        
        Args:
            compound: Composto do pneu
            laps_used: Número de voltas que o pneu já rodou
        
        Returns:
            Penalidade de tempo em segundos (quanto mais, pior)
        """
        if compound not in TyreModel.TYRE_PROPERTIES:
            return 0.0
        
        properties = TyreModel.TYRE_PROPERTIES[compound]
        degradation_rate = properties["degradation_rate"]
        
        # Penalidade linear baseada no desgaste acumulado
        # Quanto mais voltas, mais lento fica
        penalty = degradation_rate * laps_used
        
        # Aplica uma curva de degradação (não linear após certo ponto)
        # Após 70% da vida útil, degrada mais rápido
        max_laps = properties["max_laps"]
        if laps_used > max_laps * 0.7:
            # Acelera degradação nos últimos 30% da vida
            excess_laps = laps_used - (max_laps * 0.7)
            penalty += excess_laps * degradation_rate * 0.5
        
        return penalty
    
    @staticmethod
    def get_speed_bonus(compound: TyreCompound) -> float:
        """
        Retorna o bônus de velocidade do composto (valores negativos = mais rápido).
        
        Args:
            compound: Composto do pneu
        
        Returns:
            Bônus de velocidade em segundos (negativo = mais rápido)
        """
        if compound not in TyreModel.TYRE_PROPERTIES:
            return 0.0
        
        return TyreModel.TYRE_PROPERTIES[compound]["speed_bonus"]
    
    @staticmethod
    def get_dry_compounds() -> list[TyreCompound]:
        """Retorna lista de compostos para condições secas."""
        return [TyreCompound.SOFT, TyreCompound.MEDIUM, TyreCompound.HARD]
    
    @staticmethod
    def get_wet_compounds() -> list[TyreCompound]:
        """Retorna lista de compostos para condições molhadas."""
        return [TyreCompound.INTER, TyreCompound.WET]

