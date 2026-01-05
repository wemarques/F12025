"""
Endpoint para simulação de corrida F1.
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, List, Optional
from app.simulation.models import DriverSim
from app.simulation.engine import simulate_race
from app.services.fantasy_data import load_assets
from app.services.race_setup import get_race_parameters
import random

router = APIRouter()


class SimulationRequest(BaseModel):
    gp_name: str
    num_simulations: int = 100


def convert_drivers_to_sim_drivers(drivers_df, laps: int = 58) -> List[DriverSim]:
    """
    Converte DataFrame de pilotos para lista de DriverSim.
    Usa predicted_points como base para calcular tempos base e consistência.
    """
    sim_drivers = []
    
    for _, driver in drivers_df.iterrows():
        # Usa predicted_points para estimar performance
        # Pilotos com mais pontos previstos = tempos base menores (mais rápidos)
        base_points = driver.get('predicted_points', 15.0)
        
        # Converte pontos para tempo base (invertido: mais pontos = menos tempo)
        # Fórmula: tempo_base = 95 - (pontos / 2) segundos por volta
        base_lap_time = 95.0 - (base_points / 2.0)
        
        # Consistência baseada no tier (A = mais consistente, B = menos)
        if driver.get('tier') == 'A':
            consistency = 0.5 + random.uniform(-0.1, 0.2)
        else:
            consistency = 1.0 + random.uniform(-0.2, 0.3)
        
        # Degradação baseada no preço (carros mais caros tendem a ter menor degradação)
        price = driver.get('price', 15.0)
        tire_degradation = 0.15 - (price / 200.0)  # Caros: ~0.08, Baratos: ~0.15
        
        sim_drivers.append(DriverSim(
            name=driver['name'],
            base_lap_time=base_lap_time,
            consistency=consistency,
            tire_degradation=max(0.05, tire_degradation),  # Mínimo 0.05
            pit_stop_loss=20.0  # 20 segundos perdidos no pit stop
        ))
    
    return sim_drivers


@router.post("/simulate")
async def simulate_race_monte_carlo(request: SimulationRequest):
    """
    Executa simulação Monte Carlo de uma corrida (usando dados mockados).
    
    Args:
        request: SimulationRequest com gp_name e num_simulations
    
    Returns:
        Dict com estatísticas das simulações:
        - win_probabilities: Dict {driver_name: probability}
        - podium_probabilities: Dict {driver_name: probability}
        - avg_positions: Dict {driver_name: avg_position}
    """
    try:
        gp_name = request.gp_name
        num_simulations = request.num_simulations
        # Carrega dados dos pilotos
        drivers_df, _ = load_assets()
        
        # Converte para DriverSim
        sim_drivers = convert_drivers_to_sim_drivers(drivers_df)
        
        # Número de voltas (padrão para F1: ~58 voltas, varia por pista)
        # Por enquanto, fixo em 58
        laps = 58
        
        # Contadores para estatísticas
        wins = {driver.name: 0 for driver in sim_drivers}
        podiums = {driver.name: 0 for driver in sim_drivers}
        positions_sum = {driver.name: 0.0 for driver in sim_drivers}
        
        # Executa simulações Monte Carlo
        for _ in range(num_simulations):
            results = simulate_race(sim_drivers, laps)
            
            # Contabiliza vitórias (P1 - primeiro na lista ordenada)
            if results:
                wins[results[0].driver_name] += 1
            
            # Contabiliza pódios (P1, P2, P3 - primeiros 3 na lista ordenada)
            for i in range(min(3, len(results))):
                podiums[results[i].driver_name] += 1
            
            # Soma posições para média (baseado na ordem na lista)
            for position, result in enumerate(results, start=1):
                positions_sum[result.driver_name] += position
        
        # Calcula probabilidades
        win_probabilities = {
            name: (wins[name] / num_simulations) * 100 
            for name in wins.keys()
        }
        
        podium_probabilities = {
            name: (podiums[name] / num_simulations) * 100 
            for name in podiums.keys()
        }
        
        avg_positions = {
            name: positions_sum[name] / num_simulations 
            for name in positions_sum.keys()
        }
        
        # Ordena por probabilidade de vitória (maior primeiro)
        sorted_results = sorted(
            win_probabilities.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            "gp_name": gp_name,
            "num_simulations": num_simulations,
            "win_probabilities": win_probabilities,
            "podium_probabilities": podium_probabilities,
            "avg_positions": avg_positions,
            "sorted_winners": [{"driver": name, "probability": prob} for name, prob in sorted_results]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na simulação: {str(e)}")


@router.post("/run/{year}/{gp}")
async def run_monte_carlo_simulation(
    year: int,
    gp: str,
    iterations: int = Query(default=100, ge=1, le=10000, description="Número de iterações Monte Carlo"),
    rain_probability: int = Query(default=0, ge=0, le=100, description="Probabilidade de chuva (0-100%)")
):
    """
    Executa simulação Monte Carlo usando dados reais do FastF1.
    
    Args:
        year: Ano da temporada (ex: 2024)
        gp: Nome do Grande Prêmio (ex: 'Bahrain')
        iterations: Número de iterações Monte Carlo (padrão: 100, máximo: 10000)
    
    Returns:
        JSON com predições:
        {
            "track": "Bahrain",
            "iterations": 100,
            "predictions": [
                {"driver": "VER", "win_probability": 0.85, "avg_position": 1.2},
                {"driver": "HAM", "win_probability": 0.10, "avg_position": 3.4}
            ]
        }
    """
    try:
        # Obtém parâmetros de corrida a partir de dados reais
        drivers = get_race_parameters(year, gp)
        
        # Obtém número de voltas da pista (usando um valor padrão por enquanto)
        # Futuramente pode ser extraído da sessão
        total_laps = 58  # Valor padrão, pode variar por pista
        
        # Converte rain_probability de 0-100 para 0.0-1.0
        weather_prob = rain_probability / 100.0
        
        # Contadores para estatísticas
        wins = {driver.name: 0 for driver in drivers}
        positions_sum = {driver.name: 0.0 for driver in drivers}
        points_sum = {driver.name: 0.0 for driver in drivers}
        weather_conditions_count = {}
        
        # Armazena a "iteração mais representativa" (onde o vencedor foi o mais provável)
        most_likely_winner = None
        representative_iteration = None
        max_win_prob = 0.0
        
        # Loop de Monte Carlo
        for iteration in range(iterations):
            results, weather_condition = simulate_race(drivers, total_laps, weather_prob)
            
            # Conta condições climáticas (para determinar a mais frequente)
            weather_key = weather_condition.value
            weather_conditions_count[weather_key] = weather_conditions_count.get(weather_key, 0) + 1
            
            # Guarda o vencedor (primeiro na lista ordenada)
            if results:
                winner_name = results[0].driver_name
                wins[winner_name] += 1
                
                # Calcula probabilidade de vitória temporária
                temp_win_prob = wins[winner_name] / (iteration + 1)
                
                # Armazena a iteração mais representativa (maior probabilidade de vitória até agora)
                if temp_win_prob > max_win_prob:
                    max_win_prob = temp_win_prob
                    most_likely_winner = winner_name
                    representative_iteration = results
            
            # Soma posições e pontos para média
            for result in results:
                positions_sum[result.driver_name] += result.position
                points_sum[result.driver_name] += float(result.fantasy_points)
        
        # Calcula probabilidades, posições médias e pontos médios
        predictions = []
        for driver in drivers:
            win_probability = wins[driver.name] / iterations
            avg_position = positions_sum[driver.name] / iterations
            average_fantasy_points = points_sum[driver.name] / iterations
            
            predictions.append({
                "driver": driver.name,
                "win_probability": round(win_probability, 4),
                "avg_position": round(avg_position, 2),
                "average_fantasy_points": round(average_fantasy_points, 2)
            })
        
        # Ordena por probabilidade de vitória (maior primeiro)
        predictions.sort(key=lambda x: x["win_probability"], reverse=True)
        
        # Determina a condição climática mais frequente
        most_common_weather = max(weather_conditions_count.items(), key=lambda x: x[1])[0] if weather_conditions_count else "DRY"
        
        # Prepara dados do Race Trace (da iteração mais representativa)
        race_trace_data = None
        if representative_iteration:
            lap_data = []
            for result in representative_iteration:
                lap_data.append({
                    'driver': result.driver_name,
                    'lap_history': result.lap_history,
                    'position_history': result.position_history
                })
            race_trace_data = {
                'lap_data': lap_data,
                'total_laps': total_laps
            }
        
        response_data = {
            "track": gp,
            "iterations": iterations,
            "weather_condition": most_common_weather,
            "predictions": predictions
        }
        
        # Adiciona race_trace se disponível
        if race_trace_data:
            response_data["race_trace"] = race_trace_data
        
        return response_data
    
    except HTTPException:
        # Re-raise HTTP exceptions (já têm status code apropriado)
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao executar simulação Monte Carlo: {str(e)}"
        )
