from fastapi import FastAPI
from backend.routers.predict import router as predict_router

app = FastAPI(
    title="F1 Fantasy 2025 API",
    description="API para previsões, dados e análises do projeto F1 Fantasy 2025",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API funcionando"}

# Registrar rotas
app.include_router(predict_router, prefix="/predict", tags=["Predictions"])
