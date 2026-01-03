import os

class Settings:
    PROJECT_NAME: str = "F1 2025 Prediction System"
    PROJECT_VERSION: str = "1.0.0"
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
    MODEL_PATH = os.path.join(DATA_DIR, "processed", "model.pkl")
    
    # FastF1 Cache
    CACHE_DIR = os.path.join(DATA_DIR, "external", "fastf1_cache")

settings = Settings()
