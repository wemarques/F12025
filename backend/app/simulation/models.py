"""
Modelos de dados para simulação de corrida F1.
"""
from dataclasses import dataclass, field
from typing import Set
from .tyres import TyreCompound


@dataclass
class DriverSim:
    """
    Representa um piloto na simulação.
    
    Attributes:
        name: Nome do piloto
        base_lap_time: Tempo base de volta (em segundos, ex: 80.0)
        consistency: Desvio padrão da consistência (quanto menor, mais constante)
        tire_degradation: Perda de tempo por volta devido à degradação dos pneus (em segundos, ex: 0.05)
            [DEPRECADO - mantido para compatibilidade, usar current_tyre e tyre_laps]
        pit_stop_loss: Tempo perdido no pit stop (em segundos, ex: 20.0)
        current_tyre: Composto de pneu atual
        tyre_laps: Número de voltas com o pneu atual
        compounds_used: Set de compostos já utilizados na corrida (para validar regra de 2 compostos)
    """
    name: str
    base_lap_time: float
    consistency: float
    tire_degradation: float
    pit_stop_loss: float
    current_tyre: TyreCompound = TyreCompound.SOFT
    tyre_laps: int = 0
    compounds_used: Set[TyreCompound] = field(default_factory=set)


@dataclass
class RaceResult:
    """
    Armazena o resultado de um piloto em uma corrida simulada.
    
    Attributes:
        driver_name: Nome do piloto
        total_time: Tempo total da corrida (em segundos)
        laps_completed: Número de voltas completadas
        pit_stops: Número de pit stops realizados
        fastest_lap: Tempo da volta mais rápida (em segundos)
        position: Posição final na corrida (1 = primeiro)
        fantasy_points: Pontos de Fantasy F1 baseados na posição
        lap_history: Lista de tempos acumulados a cada volta
        position_history: Lista de posições a cada volta
    """
    driver_name: str
    total_time: float
    laps_completed: int
    pit_stops: int
    fastest_lap: float
    position: int = 0
    fantasy_points: int = 0
    lap_history: list[float] = None
    position_history: list[int] = None
    
    def __post_init__(self):
        """Inicializa listas vazias se não fornecidas."""
        if self.lap_history is None:
            self.lap_history = []
        if self.position_history is None:
            self.position_history = []

