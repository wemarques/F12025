from fastapi import FastAPI
from app.core.config import settings
from app.api import pilotos, prognosticos, corridas
from app.api.endpoints import analytics, optimization, simulation, fantasy
import uvicorn

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# Include Routers
app.include_router(pilotos.router, prefix="/api/pilotos", tags=["Pilotos"])
app.include_router(prognosticos.router, prefix="/api/prognosticos", tags=["Prognósticos"])
app.include_router(corridas.router, prefix="/api/corridas", tags=["Corridas"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(optimization.router, prefix="/api/v1/optimization", tags=["optimization"])
app.include_router(simulation.router, prefix="/api/v1/simulation", tags=["simulation"])
app.include_router(fantasy.router, prefix="/api/v1/fantasy", tags=["fantasy"])

@app.get("/")
def read_root():
    return {"message": "Welcome to F1 2025 Prediction API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
