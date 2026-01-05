"""
Adapter para integração com FastF1 API.

Este módulo fornece funções para carregar dados de sessões da F1 usando FastF1,
com cache persistente local para evitar re-downloads e melhorar performance.
"""
from typing import Literal
from pathlib import Path

import fastf1
from fastapi import HTTPException
from fastf1.core import Session


# Caminho do diretório de cache (relativo ao diretório backend)
_BACKEND_DIR = Path(__file__).parent.parent.parent
CACHE_DIR = _BACKEND_DIR / "cache"


def setup_cache() -> None:
    """
    Configura e habilita o cache do FastF1.
    
    O cache é persistente e armazenado localmente no diretório `backend/cache`.
    Isso evita re-downloads desnecessários de dados já baixados, melhorando
    significativamente a performance em chamadas subsequentes.
    
    O diretório de cache será criado automaticamente se não existir.
    
    Raises:
        OSError: Se não for possível criar o diretório de cache.
    """
    # Garante que o diretório de cache existe
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Habilita o cache do FastF1
    fastf1.Cache.enable_cache(str(CACHE_DIR))


def get_session_data(
    year: int,
    grand_prix: str,
    session_type: Literal["FP1", "FP2", "FP3", "Q", "S", "SS", "R"] = "R"
) -> Session:
    """
    Carrega dados de uma sessão da F1 usando FastF1.
    
    Esta função configura o cache antes de carregar os dados e trata erros
    robustamente, levantando exceções HTTP apropriadas para o frontend.
    
    Args:
        year: Ano da temporada (ex: 2025).
        grand_prix: Nome do Grande Prêmio (ex: 'Bahrain', 'Monaco') ou Round ID.
        session_type: Tipo de sessão. 'R' para Race, 'Q' para Qualifying, etc.
            Valores possíveis: 'FP1', 'FP2', 'FP3', 'Q', 'S', 'SS', 'R'.
    
    Returns:
        Session: Objeto de sessão carregado com dados de telemetria e tempos.
    
    Raises:
        HTTPException: 
            - 503 (Service Unavailable): Se a API do FastF1 falhar, der timeout,
              ou se os dados não estiverem disponíveis.
            - 422 (Unprocessable Entity): Se os parâmetros fornecidos forem inválidos.
    """
    # Configura o cache antes de carregar dados
    try:
        setup_cache()
    except OSError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Não foi possível configurar o cache: {str(e)}"
        )
    
    try:
        # Obtém a sessão
        session = fastf1.get_session(year, grand_prix, session_type)
        
        # Carrega os dados (pode demorar na primeira vez)
        session.load()
        
        return session
        
    except ValueError as e:
        # Parâmetros inválidos (ano, GP, tipo de sessão)
        raise HTTPException(
            status_code=422,
            detail=f"Parâmetros inválidos: {str(e)}"
        )
    except Exception as e:
        # Erros genéricos da API (timeout, dados indisponíveis, etc.)
        error_msg = str(e)
        raise HTTPException(
            status_code=503,
            detail=(
                f"Serviço FastF1 indisponível ou dados não encontrados para "
                f"{year} {grand_prix} {session_type}. "
                f"Erro: {error_msg}"
            )
        )

