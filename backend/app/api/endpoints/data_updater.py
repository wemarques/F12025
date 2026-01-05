"""
Endpoint para atualização de dados da F1 usando FastF1.
"""
from fastapi import APIRouter, BackgroundTasks, HTTPException
import fastf1
from app.services.fastf1_adapter import setup_cache, get_session_data
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


def update_f1_data_task(year: int):
    """
    Função que executa o download e salvamento dos dados em segundo plano.
    
    Args:
        year: Ano da temporada para baixar dados
    """
    logger.info(f"Iniciando download dos dados da temporada {year}...")
    try:
        # Configura o cache do FastF1
        setup_cache()
        
        # Obtém o calendário da temporada
        schedule = fastf1.get_event_schedule(year)
        logger.info(f"Calendário obtido: {len(schedule)} eventos encontrados")
        
        # TODO: Quando os modelos de banco de dados forem criados, descomente:
        # from database.database import SessionLocal
        # from models import Race, Result  # Exemplo
        
        # db = SessionLocal()
        try:
            events_processed = 0
            events_failed = 0
            
            for index, row in schedule.iterrows():
                # Processa apenas corridas principais (conventional format)
                event_format = row.get("EventFormat", "")
                if event_format == "conventional":
                    event_name = row.get("EventName", f"Event {index}")
                    round_number = row.get("RoundNumber", index)
                    location = row.get("Location", "")
                    
                    logger.info(f"Baixando dados para: {event_name} (Round {round_number})")
                    
                    try:
                        # Tenta baixar dados da corrida (Race)
                        session = get_session_data(year, round_number, "R")
                        
                        if session and hasattr(session, 'laps') and session.laps is not None:
                            # LÓGICA PARA SALVAR NO BANCO DE DADOS
                            # TODO: Implementar quando os modelos estiverem prontos
                            # Exemplo:
                            # race = Race(
                            #     year=year,
                            #     round_number=round_number,
                            #     name=event_name,
                            #     location=location
                            # )
                            # db.add(race)
                            # 
                            # # Processar resultados dos pilotos
                            # if hasattr(session, 'results'):
                            #     for driver_result in session.results:
                            #         result = Result(
                            #             race_id=race.id,
                            #             driver_name=driver_result['Abbreviation'],
                            #             position=driver_result['Position'],
                            #             points=driver_result['Points'],
                            #             # ... outros campos
                            #         )
                            #         db.add(result)
                            # 
                            # db.commit()
                            
                            events_processed += 1
                            logger.info(f"✓ Dados baixados com sucesso: {event_name}")
                        else:
                            logger.warning(f"⚠ Sessão sem dados válidos: {event_name}")
                            events_failed += 1
                            
                    except HTTPException as e:
                        logger.error(f"✗ Erro HTTP ao baixar {event_name}: {e.detail}")
                        events_failed += 1
                    except Exception as e:
                        logger.error(f"✗ Erro ao processar {event_name}: {str(e)}")
                        events_failed += 1
                        
            logger.info(
                f"Atualização concluída. Processados: {events_processed}, "
                f"Falhas: {events_failed}, Total: {events_processed + events_failed}"
            )
            
        except Exception as e:
            logger.error(f"Erro durante o processamento do calendário: {str(e)}")
            # db.rollback()
            raise
        finally:
            # db.close()
            pass
            
    except Exception as e:
        logger.error(f"Erro crítico durante a atualização: {str(e)}")
        # db.rollback() se necessário
        raise


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
    from datetime import datetime
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
    
    TODO: Implementar rastreamento de status quando o sistema de jobs estiver pronto.
    Por enquanto, retorna informações básicas.
    """
    return {
        "message": "Status de atualização não implementado ainda.",
        "note": "Esta funcionalidade será implementada quando os modelos de banco de dados estiverem prontos."
    }

