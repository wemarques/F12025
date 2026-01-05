from pydantic import BaseModel

class PredictionRequest(BaseModel):
    driver: str
    team: str
    quali_position: int
    race_position: int
