from fastapi import FastAPI
from app.core.config import settings
from app.api import pilotos, prognosticos, corridas
import uvicorn

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# Include Routers
app.include_router(pilotos.router, prefix="/api/pilotos", tags=["Pilotos"])
app.include_router(prognosticos.router, prefix="/api/prognosticos", tags=["Prognósticos"])
app.include_router(corridas.router, prefix="/api/corridas", tags=["Corridas"])

@app.get("/")
def read_root():
    return {"message": "Welcome to F1 2025 Prediction API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
