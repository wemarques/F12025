"""
Endpoint para atualização de dados da F1 usando FastF1.
"""
from fastapi import APIRouter, BackgroundTasks, HTTPException
import fastf1
from app.services.fastf1_adapter import setup_cache, get_session_data
from database.database import SessionLocal
from models.f1_models import Driver, Team, Race, Result, Lap, UpdateJob
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


def get_or_create_driver(db, abbreviation: str, full_name: str = None, number: int = None, team_name: str = None):
    """
    Obtém ou cria um piloto no banco de dados.
    
    Args:
        db: Sessão do banco de dados
        abbreviation: Abreviação do piloto (ex: VER, HAM)
        full_name: Nome completo do piloto
        number: Número do piloto
        team_name: Nome da equipe
    
    Returns:
        Driver: Objeto do piloto
    """
    driver = db.query(Driver).filter(Driver.abbreviation == abbreviation).first()
    
    if not driver:
        driver = Driver(
            abbreviation=abbreviation,
            full_name=full_name or abbreviation,
            number=number,
            team_name=team_name
        )
        db.add(driver)
        db.flush()  # Para obter o ID sem fazer commit
        logger.info(f"✓ Novo piloto criado: {abbreviation}")
    else:
        # Atualiza informações se fornecidas
        if full_name:
            driver.full_name = full_name
        if number:
            driver.number = number
        if team_name:
            driver.team_name = team_name
        driver.updated_at = datetime.utcnow()
    
    return driver


def get_or_create_team(db, team_name: str):
    """
    Obtém ou cria uma equipe no banco de dados.
    
    Args:
        db: Sessão do banco de dados
        team_name: Nome da equipe
    
    Returns:
        Team: Objeto da equipe
    """
    if not team_name:
        return None
        
    team = db.query(Team).filter(Team.name == team_name).first()
    
    if not team:
        team = Team(name=team_name, full_name=team_name)
        db.add(team)
        db.flush()
        logger.info(f"✓ Nova equipe criada: {team_name}")
    
    return team


def update_f1_data_task(year: int):
    """
    Função que executa o download e salvamento dos dados em segundo plano.
    
    Args:
        year: Ano da temporada para baixar dados
    """
    logger.info(f"Iniciando download dos dados da temporada {year}...")
    db = SessionLocal()
    
    # Cria um job de atualização para rastreamento
    job = UpdateJob(year=year, status="running", started_at=datetime.utcnow())
    db.add(job)
    db.commit()
    
    try:
        # Configura o cache do FastF1
        setup_cache()
        
        # Obtém o calendário da temporada
        schedule = fastf1.get_event_schedule(year)
        logger.info(f"Calendário obtido: {len(schedule)} eventos encontrados")
        
        job.total_events = len(schedule)
        db.commit()
        
        events_processed = 0
        events_failed = 0
        
        for index, row in schedule.iterrows():
            # Processa apenas corridas principais (conventional format)
            event_format = row.get("EventFormat", "")
            if event_format == "conventional":
                event_name = row.get("EventName", f"Event {index}")
                round_number = int(row.get("RoundNumber", index))
                location = row.get("Location", "")
                country = row.get("Country", "")
                event_date = row.get("EventDate", None)
                
                logger.info(f"Baixando dados para: {event_name} (Round {round_number})")
                
                try:
                    # Tenta baixar dados da corrida (Race)
                    session = get_session_data(year, round_number, "R")
                    
                    if session and hasattr(session, 'laps') and session.laps is not None:
                        # Verifica se a corrida já existe
                        race = db.query(Race).filter(
                            Race.year == year,
                            Race.round_number == round_number
                        ).first()
                        
                        if not race:
                            # Cria nova corrida
                            race = Race(
                                year=year,
                                round_number=round_number,
                                event_name=event_name,
                                location=location,
                                country=country,
                                event_date=event_date,
                                event_format=event_format,
                                session_type="R"
                            )
                            db.add(race)
                            db.flush()
                            logger.info(f"✓ Corrida criada: {event_name}")
                        else:
                            logger.info(f"⚠ Corrida já existe, atualizando dados: {event_name}")
                            # Remove resultados e voltas antigas para atualizar
                            db.query(Result).filter(Result.race_id == race.id).delete()
                            db.query(Lap).filter(Lap.race_id == race.id).delete()
                        
                        # Processa resultados dos pilotos
                        if hasattr(session, 'results') and session.results is not None:
                            results_df = session.results
                            
                            for idx, driver_result in results_df.iterrows():
                                try:
                                    abbreviation = str(driver_result.get('Abbreviation', ''))
                                    if not abbreviation:
                                        continue
                                    
                                    full_name = str(driver_result.get('FullName', abbreviation))
                                    driver_number = driver_result.get('DriverNumber', None)
                                    team_name = str(driver_result.get('TeamName', ''))
                                    
                                    # Cria ou obtém piloto
                                    driver = get_or_create_driver(
                                        db, 
                                        abbreviation, 
                                        full_name, 
                                        int(driver_number) if driver_number else None,
                                        team_name
                                    )
                                    
                                    # Cria ou obtém equipe
                                    team = get_or_create_team(db, team_name) if team_name else None
                                    
                                    # Cria resultado
                                    result = Result(
                                        race_id=race.id,
                                        driver_id=driver.id,
                                        team_id=team.id if team else None,
                                        position=int(driver_result.get('Position', 0)) if driver_result.get('Position') else None,
                                        grid_position=int(driver_result.get('GridPosition', 0)) if driver_result.get('GridPosition') else None,
                                        points=float(driver_result.get('Points', 0)) if driver_result.get('Points') else None,
                                        status=str(driver_result.get('Status', '')),
                                        time=str(driver_result.get('Time', '')) if driver_result.get('Time') else None
                                    )
                                    db.add(result)
                                    
                                except Exception as e:
                                    logger.error(f"✗ Erro ao processar resultado do piloto {abbreviation}: {str(e)}")
                                    continue
                        
                        # Processa voltas
                        if hasattr(session, 'laps') and session.laps is not None and len(session.laps) > 0:
                            laps_df = session.laps
                            laps_saved = 0
                            
                            for idx, lap_data in laps_df.iterrows():
                                try:
                                    abbreviation = str(lap_data.get('Driver', ''))
                                    if not abbreviation:
                                        continue
                                    
                                    # Obtém o piloto (já deve existir dos resultados)
                                    driver = db.query(Driver).filter(Driver.abbreviation == abbreviation).first()
                                    if not driver:
                                        continue
                                    
                                    lap_number = int(lap_data.get('LapNumber', 0))
                                    if lap_number == 0:
                                        continue
                                    
                                    # Converte lap_time para segundos
                                    lap_time_obj = lap_data.get('LapTime')
                                    lap_time_seconds = None
                                    lap_time_str = None
                                    
                                    if lap_time_obj is not None:
                                        try:
                                            # FastF1 retorna timedelta
                                            lap_time_seconds = lap_time_obj.total_seconds()
                                            lap_time_str = str(lap_time_obj)
                                        except:
                                            pass
                                    
                                    # Cria volta
                                    lap = Lap(
                                        race_id=race.id,
                                        driver_id=driver.id,
                                        lap_number=lap_number,
                                        lap_time=lap_time_seconds,
                                        lap_time_str=lap_time_str,
                                        position=int(lap_data.get('Position', 0)) if lap_data.get('Position') else None,
                                        compound=str(lap_data.get('Compound', '')) if lap_data.get('Compound') else None,
                                        tyre_life=int(lap_data.get('TyreLife', 0)) if lap_data.get('TyreLife') else None,
                                        is_personal_best=bool(lap_data.get('IsPersonalBest', False)),
                                        is_accurate=bool(lap_data.get('IsAccurate', True))
                                    )
                                    db.add(lap)
                                    laps_saved += 1
                                    
                                except Exception as e:
                                    logger.error(f"✗ Erro ao processar volta: {str(e)}")
                                    continue
                            
                            logger.info(f"✓ {laps_saved} voltas salvas para {event_name}")
                        
                        # Commit após processar cada corrida
                        db.commit()
                        events_processed += 1
                        logger.info(f"✓ Dados salvos com sucesso: {event_name}")
                        
                    else:
                        logger.warning(f"⚠ Sessão sem dados válidos: {event_name}")
                        events_failed += 1
                        
                except HTTPException as e:
                    logger.error(f"✗ Erro HTTP ao baixar {event_name}: {e.detail}")
                    events_failed += 1
                    db.rollback()
                except Exception as e:
                    logger.error(f"✗ Erro ao processar {event_name}: {str(e)}")
                    events_failed += 1
                    db.rollback()
                
                # Atualiza o job
                job.events_processed = events_processed
                job.events_failed = events_failed
                db.commit()
        
        # Finaliza o job
        job.status = "completed"
        job.completed_at = datetime.utcnow()
        db.commit()
        
        logger.info(
            f"Atualização concluída. Processados: {events_processed}, "
            f"Falhas: {events_failed}, Total: {events_processed + events_failed}"
        )
        
    except Exception as e:
        logger.error(f"Erro crítico durante a atualização: {str(e)}")
        job.status = "failed"
        job.error_message = str(e)
        job.completed_at = datetime.utcnow()
        db.commit()
        raise
    finally:
        db.close()


@router.post("/update-season-data/{year}", status_code=202)
async def trigger_update(year: int, background_tasks: BackgroundTasks):
    """
    Dispara a atualização dos dados de uma temporada da F1 em segundo plano.
    
    Args:
        year: Ano da temporada (ex: 2024, 2025)
        background_tasks: BackgroundTasks do FastAPI para execução assíncrona
    
    Returns:
        dict: Mensagem de confirmação com status 202 (Accepted)
    
    Raises:
        HTTPException: Se o ano for inválido (< 2018)
    """
    # FastF1 tem dados mais completos a partir de 2018
    if year < 2018:
        raise HTTPException(
            status_code=400,
            detail="Dados completos disponíveis apenas a partir de 2018."
        )
    
    # Valida ano máximo (ex: não permitir anos futuros muito distantes)
    current_year = datetime.now().year
    if year > current_year + 1:
        raise HTTPException(
            status_code=400,
            detail=f"Ano inválido. Máximo permitido: {current_year + 1}"
        )
    
    # Adiciona a tarefa em background
    background_tasks.add_task(update_f1_data_task, year)
    
    return {
        "message": f"Atualização dos dados da temporada {year} iniciada em segundo plano.",
        "status": "accepted",
        "year": year
    }


@router.get("/update-status")
async def get_update_status():
    """
    Endpoint para verificar o status das atualizações.
    
    Returns:
        dict: Status dos jobs de atualização mais recentes
    """
    db = SessionLocal()
    try:
        # Busca os últimos 10 jobs
        jobs = db.query(UpdateJob).order_by(UpdateJob.started_at.desc()).limit(10).all()
        
        jobs_data = []
        for job in jobs:
            jobs_data.append({
                "id": job.id,
                "year": job.year,
                "status": job.status,
                "events_processed": job.events_processed,
                "events_failed": job.events_failed,
                "total_events": job.total_events,
                "started_at": job.started_at.isoformat() if job.started_at else None,
                "completed_at": job.completed_at.isoformat() if job.completed_at else None,
                "error_message": job.error_message
            })
        
        return {
            "message": "Status de atualização obtido com sucesso.",
            "jobs": jobs_data
        }
    finally:
        db.close()


@router.post("/init-database", status_code=200)
async def init_database():
    """
    Endpoint para inicializar o banco de dados criando todas as tabelas.
    
    Este endpoint deve ser chamado apenas uma vez após o deploy inicial
    ou quando houver mudanças nos modelos que exijam recriação das tabelas.
    
    Returns:
        dict: Mensagem de confirmação com lista de tabelas criadas
    
    Raises:
        HTTPException: Se houver erro ao criar as tabelas
    """
    try:
        from database.database import Base, engine
        from sqlalchemy import inspect
        
        logger.info("Iniciando criação das tabelas no banco de dados...")
        
        # Cria todas as tabelas
        Base.metadata.create_all(bind=engine)
        
        # Verifica as tabelas criadas
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        logger.info(f"✓ {len(tables)} tabelas criadas com sucesso")
        
        return {
            "message": "Banco de dados inicializado com sucesso!",
            "tables_created": len(tables),
            "tables": sorted(tables)
        }
        
    except Exception as e:
        logger.error(f"✗ Erro ao inicializar banco de dados: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao inicializar banco de dados: {str(e)}"
        )
