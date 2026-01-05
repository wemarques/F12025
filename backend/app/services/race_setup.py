"""
Serviço para configurar parâmetros de corrida a partir de dados reais do FastF1.
"""
import numpy as np
from typing import List
from fastapi import HTTPException

from app.services.fastf1_adapter import get_session_data
from app.simulation.models import DriverSim


def get_race_parameters(year: int, gp_name: str) -> List[DriverSim]:
    """
    Obtém parâmetros de corrida a partir de dados reais do FastF1.
    
    Carrega dados de uma sessão (Race ou Qualifying) e extrai parâmetros
    de performance de cada piloto para uso na simulação.
    
    Args:
        year: Ano da temporada (ex: 2024, 2025)
        gp_name: Nome do Grande Prêmio (ex: 'Bahrain', 'Monaco')
    
    Returns:
        Lista de objetos DriverSim com parâmetros calculados a partir dos dados reais.
    
    Raises:
        HTTPException:
            - 503: Se não conseguir carregar dados do FastF1
            - 404: Se não houver dados suficientes (ex: poucos pilotos ou voltas)
    """
    # Tenta carregar sessão de Race primeiro, depois Qualifying
    session = None
    session_type = None
    
    try:
        session = get_session_data(year, gp_name, "R")
        session_type = "Race"
    except HTTPException:
        # Se Race não existir, tenta Qualifying
        try:
            session = get_session_data(year, gp_name, "Q")
            session_type = "Qualifying"
        except HTTPException as e:
            raise HTTPException(
                status_code=503,
                detail=f"Não foi possível carregar dados de Race ou Qualifying para {year} {gp_name}: {str(e)}"
            )
    
    # Verifica se a sessão tem dados
    if not hasattr(session, 'laps') or session.laps is None:
        raise HTTPException(
            status_code=404,
            detail=f"Sessão {session_type} para {year} {gp_name} não possui dados de voltas."
        )
    
    drivers_list = []
    
    # Obtém lista única de pilotos
    unique_drivers = session.laps['Driver'].unique()
    
    if len(unique_drivers) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum piloto encontrado na sessão {session_type} para {year} {gp_name}."
        )
    
    # Para cada piloto, calcula parâmetros
    for driver_code in unique_drivers:
        try:
            # Pega voltas do piloto (sem pit stops e voltas rápidas)
            driver_laps = (
                session.laps
                .pick_drivers(driver_code)
                .pick_wo_box()  # Remove voltas com pit stops
                .pick_quicklaps()  # Pega apenas voltas rápidas (remove outliers)
            )
            
            # Verifica se tem voltas válidas
            if driver_laps.empty or len(driver_laps) < 2:
                # Se não tiver voltas válidas, pula este piloto
                continue
            
            # Pega os tempos de volta (em segundos)
            lap_times = driver_laps['LapTime'].dt.total_seconds()
            
            # Remove valores NaN ou infinitos
            lap_times = lap_times.dropna()
            lap_times = lap_times[np.isfinite(lap_times)]
            
            if len(lap_times) < 2:
                continue
            
            # Calcula média (base_lap_time)
            base_lap_time = float(lap_times.mean())
            
            # Calcula desvio padrão (consistency)
            consistency = float(lap_times.std())
            
            # Se consistency for muito baixa ou zero, define um mínimo
            if consistency < 0.1:
                consistency = 0.1
            
            # Heurística de pneu: valores padrão
            # (difícil extrair isso só da telemetria básica)
            tire_degradation = 0.1  # 0.1 segundos por volta
            pit_stop_loss = 24.0  # 24 segundos perdidos no pit stop
            
            # Obtém nome completo do piloto (tenta obter da sessão)
            try:
                driver_info = session.get_driver(driver_code)
                driver_name = driver_info.FullName if hasattr(driver_info, 'FullName') else driver_code
            except:
                # Se não conseguir, usa o código do piloto
                driver_name = driver_code
            
            # Cria objeto DriverSim
            driver_sim = DriverSim(
                name=driver_name,
                base_lap_time=base_lap_time,
                consistency=consistency,
                tire_degradation=tire_degradation,
                pit_stop_loss=pit_stop_loss
            )
            
            drivers_list.append(driver_sim)
            
        except Exception as e:
            # Se houver erro ao processar um piloto, continua com os outros
            continue
    
    # Verifica se conseguiu processar pelo menos alguns pilotos
    if len(drivers_list) < 2:
        raise HTTPException(
            status_code=404,
            detail=f"Dados insuficientes: apenas {len(drivers_list)} piloto(s) com voltas válidas encontrado(s) para {year} {gp_name}."
        )
    
    return drivers_list

