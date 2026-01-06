from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import settings, use defaults if not available
try:
    from app.core.config import settings
    PROJECT_NAME = settings.PROJECT_NAME
    PROJECT_VERSION = settings.PROJECT_VERSION
except Exception as e:
    logger.warning(f"Could not import settings: {e}. Using defaults.")
    PROJECT_NAME = "F1 2025 Prediction System"
    PROJECT_VERSION = "1.0.0"

app = FastAPI(title=PROJECT_NAME, version=PROJECT_VERSION)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and register routers with error handling
routers_to_register = []

# Try to import legacy routers
try:
    from app.api import pilotos, prognosticos, corridas
    routers_to_register.extend([
        (pilotos.router, "/api/pilotos", ["Pilotos"]),
        (prognosticos.router, "/api/prognosticos", ["Prognósticos"]),
        (corridas.router, "/api/corridas", ["Corridas"]),
    ])
    logger.info("✓ Legacy routers imported successfully")
except Exception as e:
    logger.warning(f"Could not import legacy routers: {e}")

# Try to import new endpoint routers
try:
    from app.api.endpoints import analytics, optimization, simulation, fantasy, data_updater
    routers_to_register.extend([
        (analytics.router, "/api/v1/analytics", ["analytics"]),
        (optimization.router, "/api/v1/optimization", ["optimization"]),
        (simulation.router, "/api/v1/simulation", ["simulation"]),
        (fantasy.router, "/api/v1/fantasy", ["fantasy"]),
        (data_updater.router, "/api/v1/data", ["data-updater"]),
    ])
    logger.info("✓ New endpoint routers imported successfully")
except Exception as e:
    logger.warning(f"Could not import new endpoint routers: {e}")

# Register all successfully imported routers
for router, prefix, tags in routers_to_register:
    try:
        app.include_router(router, prefix=prefix, tags=tags)
        logger.info(f"✓ Registered router: {prefix}")
    except Exception as e:
        logger.error(f"✗ Failed to register router {prefix}: {e}")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to F1 2025 Prediction API",
        "version": PROJECT_VERSION,
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/health")
def health_check():
    registered_routes = [
        {"path": route.path, "methods": list(route.methods)}
        for route in app.routes
        if hasattr(route, 'path') and hasattr(route, 'methods')
    ]
    return {
        "status": "healthy",
        "version": PROJECT_VERSION,
        "routes_count": len(registered_routes),
        "routes": registered_routes
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
