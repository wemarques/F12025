import fastf1
import pandas as pd
from app.core.config import settings
import os

# Enable cache
if not os.path.exists(settings.CACHE_DIR):
    os.makedirs(settings.CACHE_DIR)
fastf1.Cache.enable_cache(settings.CACHE_DIR)

def load_session_data(year: int, gp: str, session_type: str = 'R'):
    """
    Load FastF1 session data.
    session_type: 'R' for Race, 'Q' for Qualifying, etc.
    """
    session = fastf1.get_session(year, gp, session_type)
    session.load()
    
    return session

def get_weather_data(session):
    return session.weather_data

def get_laps_data(session):
    return session.laps

def get_stint_data(session):
    laps = session.laps
    stints = laps[['Driver', 'Stint', 'Compound', 'TyreLife', 'LapNumber']].copy()
    return stints
