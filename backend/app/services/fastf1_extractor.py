import fastf1
import os
from app.core.config import settings

def carregar_sessao(ano: int, corrida: str, tipo_sessao: str = 'R'):
    """
    Carrega uma sessão do FastF1 com cache habilitado.
    
    Args:
        ano (int): Ano da temporada (ex: 2025).
        corrida (str): Nome do GP (ex: 'Bahrain', 'Monaco') ou Round ID.
        tipo_sessao (str): Identificador da sessão ('FP1', 'FP2', 'FP3', 'Q', 'S', 'SS', 'R').
        
    Returns:
        fastf1.core.Session: Objeto de sessão carregado com dados de telemetria e tempos.
    """
    # Garante que o diretório de cache existe
    if not os.path.exists(settings.CACHE_DIR):
        os.makedirs(settings.CACHE_DIR, exist_ok=True)
    
    # Habilita o cache para otimizar chamadas subsequentes
    fastf1.Cache.enable_cache(settings.CACHE_DIR)
    
    try:
        session = fastf1.get_session(ano, corrida, tipo_sessao)
        session.load()
        return session
    except Exception as e:
        print(f"Erro ao carregar sessão {ano} {corrida} {tipo_sessao}: {str(e)}")
        return None
