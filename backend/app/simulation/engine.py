"""
Motor de simulação de corrida F1.
"""
import random
import copy
from typing import List, Tuple
from .models import DriverSim, RaceResult
from .weather import WeatherEngine, WeatherCondition
from .tyres import TyreModel, TyreCompound

# Sistema de pontuação F1 (baseado na posição final)
F1_POINTS_SYSTEM = {
    1: 25,   # 1º lugar
    2: 18,   # 2º lugar
    3: 15,   # 3º lugar
    4: 12,   # 4º lugar
    5: 10,   # 5º lugar
    6: 8,    # 6º lugar
    7: 6,    # 7º lugar
    8: 4,    # 8º lugar
    9: 2,    # 9º lugar
    10: 1    # 10º lugar
    # Posições 11-20: 0 pontos
}


def _choose_next_tyre(
    driver: DriverSim,
    weather: WeatherCondition,
    laps_remaining: int,
    pit_stop_loss: float
) -> TyreCompound:
    """
    Escolhe o próximo composto de pneu para troca.
    
    Args:
        driver: Piloto com estado atual
        weather: Condição climática
        laps_remaining: Voltas restantes na corrida
        pit_stop_loss: Tempo perdido no pit stop
    
    Returns:
        Próximo composto a usar
    """
    # Se estiver chovendo, usa pneu de chuva
    if weather != WeatherCondition.DRY:
        if weather == WeatherCondition.WET:
            return TyreCompound.WET
        else:  # MIXED
            # Em condições mistas, usa Intermediate
            return TyreCompound.INTER
    
    # Em condições secas, escolhe baseado na estratégia
    dry_compounds = TyreModel.get_dry_compounds()
    
    # Se ainda não usou 2 compostos diferentes, escolhe um que falta
    if len(driver.compounds_used) < 2:
        available = [c for c in dry_compounds if c not in driver.compounds_used]
        if available:
            # Escolhe o mais rápido disponível se faltam muitas voltas, senão o mais durável
            if laps_remaining > 20:
                # Prefere SOFT se faltam muitas voltas (pode trocar depois)
                if TyreCompound.SOFT in available:
                    return TyreCompound.SOFT
                elif TyreCompound.MEDIUM in available:
                    return TyreCompound.MEDIUM
                else:
                    return TyreCompound.HARD
            else:
                # Se faltam poucas voltas, escolhe o mais rápido
                if TyreCompound.SOFT in available:
                    return TyreCompound.SOFT
                elif TyreCompound.MEDIUM in available:
                    return TyreCompound.MEDIUM
                else:
                    return TyreCompound.HARD
    
    # Se já usou 2 compostos, escolhe o melhor para chegar ao fim
    # Prefere HARD se faltam muitas voltas, senão MEDIUM ou SOFT
    if laps_remaining > 25:
        return TyreCompound.HARD
    elif laps_remaining > 15:
        return TyreCompound.MEDIUM
    else:
        return TyreCompound.SOFT


def simulate_race(
    drivers: list[DriverSim],
    total_laps: int,
    weather_prob: float = 0.0
) -> Tuple[list[RaceResult], WeatherCondition]:
    """
    Simula uma corrida F1 completa.
    
    Args:
        drivers: Lista de pilotos para a simulação
        total_laps: Número total de voltas da corrida
        weather_prob: Probabilidade de chuva (0.0 a 1.0, onde 1.0 = chuva garantida)
    
    Returns:
        Tupla (lista de RaceResult ordenada por tempo total, WeatherCondition)
    """
    # Determina a condição climática da corrida
    weather_condition = WeatherEngine.determine_weather(weather_prob)
    
    # Cria cópias dos pilotos para não modificar os originais
    race_drivers = []
    for driver in drivers:
        driver_copy = copy.deepcopy(driver)
        # Inicializa com pneu inicial (SOFT ou MEDIUM)
        driver_copy.current_tyre = random.choice([TyreCompound.SOFT, TyreCompound.MEDIUM])
        driver_copy.tyre_laps = 0
        driver_copy.compounds_used = {driver_copy.current_tyre}
        race_drivers.append(driver_copy)
    
    # Estrutura para rastrear tempos e posições a cada volta
    driver_times = {driver.name: 0.0 for driver in race_drivers}
    driver_results = {}
    
    # Prepara objetos RaceResult para cada piloto
    for driver in race_drivers:
        driver_results[driver.name] = RaceResult(
            driver_name=driver.name,
            total_time=0.0,
            laps_completed=0,
            pit_stops=0,
            fastest_lap=float('inf'),
            lap_history=[],
            position_history=[]
        )
    
    # Loop por cada volta
    for lap in range(1, total_laps + 1):
        laps_remaining = total_laps - lap + 1
        
        # Para cada piloto, simula a volta
        for driver in race_drivers:
            result = driver_results[driver.name]
            
            # Calcula penalidade do pneu atual
            tyre_penalty = TyreModel.get_lap_penalty(driver.current_tyre, driver.tyre_laps)
            tyre_bonus = TyreModel.get_speed_bonus(driver.current_tyre)
            
            # Calcula o tempo da volta: base + variação aleatória + penalidade do pneu - bônus do pneu
            lap_time = (
                random.gauss(driver.base_lap_time, driver.consistency) +
                tyre_penalty -
                tyre_bonus
            )
            
            # Aplica impacto do clima
            lap_time = WeatherEngine.apply_weather_impact(lap_time, weather_condition, driver_skill=1.0)
            
            # Adiciona ao tempo total acumulado
            driver_times[driver.name] += lap_time
            
            # Atualiza volta mais rápida
            if lap_time < result.fastest_lap:
                result.fastest_lap = lap_time
            
            # Incrementa contador de voltas do pneu
            driver.tyre_laps += 1
            
            # Decisão de pit stop (exceto na última volta)
            if lap < total_laps:
                # Calcula se vale a pena fazer pit stop
                # Se a penalidade do pneu atual for muito alta, faz pit stop
                current_penalty = TyreModel.get_lap_penalty(driver.current_tyre, driver.tyre_laps)
                
                # Estima penalidade média para as voltas restantes se continuar com este pneu
                estimated_future_penalty = TyreModel.get_lap_penalty(
                    driver.current_tyre,
                    driver.tyre_laps + laps_remaining // 2
                )
                
                # Estima tempo médio por volta com pneu novo
                next_tyre = _choose_next_tyre(driver, weather_condition, laps_remaining - 1, driver.pit_stop_loss)
                new_tyre_penalty = TyreModel.get_lap_penalty(next_tyre, 0)
                new_tyre_bonus = TyreModel.get_speed_bonus(next_tyre)
                new_tyre_avg_time = driver.base_lap_time + new_tyre_penalty - new_tyre_bonus
                
                # Tempo médio por volta com pneu atual
                current_avg_time = driver.base_lap_time + estimated_future_penalty - TyreModel.get_speed_bonus(driver.current_tyre)
                
                # Se o custo de continuar (tempo perdido por volta * voltas restantes) 
                # for maior que o custo do pit (tempo do pit + tempo melhor nas voltas restantes)
                cost_to_continue = (current_avg_time - new_tyre_avg_time) * laps_remaining
                cost_to_pit = driver.pit_stop_loss
                
                # Também considera se o pneu já está muito desgastado
                tyre_props = TyreModel.TYRE_PROPERTIES.get(driver.current_tyre, {})
                max_laps = tyre_props.get("max_laps", 30)
                is_tyre_worn = driver.tyre_laps >= max_laps * 0.8
                
                # Faz pit stop se:
                # 1. O pneu está muito desgastado (80% da vida útil), OU
                # 2. O custo de continuar supera o custo do pit stop
                if is_tyre_worn or (cost_to_continue > cost_to_pit and laps_remaining > 5):
                    # Faz pit stop
                    driver_times[driver.name] += driver.pit_stop_loss
                    result.pit_stops += 1
                    
                    # Escolhe próximo pneu
                    next_tyre = _choose_next_tyre(driver, weather_condition, laps_remaining - 1, driver.pit_stop_loss)
                    driver.current_tyre = next_tyre
                    driver.tyre_laps = 0
                    driver.compounds_used.add(next_tyre)
        
        # Após cada volta, calcula posições atuais e grava histórico
        # Ordena pilotos por tempo total atual
        sorted_drivers = sorted(driver_times.items(), key=lambda x: x[1])
        
        # Atualiza posição e histórico de cada piloto
        for position, (driver_name, _) in enumerate(sorted_drivers, start=1):
            result = driver_results[driver_name]
            result.position_history.append(position)
            result.lap_history.append(driver_times[driver_name])
    
    # Finaliza resultados
    results = []
    for driver in race_drivers:
        result = driver_results[driver.name]
        result.total_time = driver_times[driver.name]
        result.laps_completed = total_laps
        results.append(result)
    
    # Ordena por tempo total (menor tempo vence)
    results.sort(key=lambda x: x.total_time)
    
    # Atribui posição final e calcula pontos para cada resultado
    for position, result in enumerate(results, start=1):
        # Calcula pontos baseado na posição (1 = primeiro)
        result.fantasy_points = F1_POINTS_SYSTEM.get(position, 0)
        result.position = position
    
    return results, weather_condition


if __name__ == "__main__":
    # Teste rápido
    print("=" * 60)
    print("TESTE DE SIMULAÇÃO DE CORRIDA F1")
    print("=" * 60)
    
    # Cria 2 pilotos: "Verstappen" (Rápido e constante) e "Sargeant" (Mais lento e irregular)
    drivers = [
        DriverSim(
            name="Verstappen",
            base_lap_time=80.0,  # Rápido
            consistency=0.3,  # Constante (baixo desvio padrão)
            tire_degradation=0.05,  # Baixa degradação (deprecado, mantido para compatibilidade)
            pit_stop_loss=20.0
        ),
        DriverSim(
            name="Sargeant",
            base_lap_time=82.0,  # Mais lento
            consistency=1.2,  # Irregular (alto desvio padrão)
            tire_degradation=0.08,  # Maior degradação (deprecado)
            pit_stop_loss=20.0
        )
    ]
    
    # Roda uma corrida de 50 voltas
    total_laps = 50
    
    print(f"\nSimulando corrida com {len(drivers)} pilotos e {total_laps} voltas...\n")
    
    results, weather = simulate_race(drivers, total_laps, weather_prob=0.0)
    print(f"Condição climática: {weather.value}\n")
    
    # Imprime o vencedor e quantos pit stops cada um fez
    print("RESULTADOS DA CORRIDA:")
    print("-" * 60)
    print(f"{'Pos':<5} {'Piloto':<15} {'Tempo Total (s)':<18} {'Pit Stops':<12} {'Volta Mais Rápida (s)':<20}")
    print("-" * 60)
    
    for i, result in enumerate(results, start=1):
        print(f"{i:<5} {result.driver_name:<15} {result.total_time:<18.2f} {result.pit_stops:<12} {result.fastest_lap:<20.3f}")
    
    print("-" * 60)
    print(f"\nVENCEDOR: {results[0].driver_name}")
    print(f"   Tempo: {results[0].total_time:.2f}s | Pit Stops: {results[0].pit_stops}")
    print(f"\n2º Lugar: {results[1].driver_name}")
    print(f"   Tempo: {results[1].total_time:.2f}s | Pit Stops: {results[1].pit_stops}")
    print("\nSimulação concluída com sucesso!")
