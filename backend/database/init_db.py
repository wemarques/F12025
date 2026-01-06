"""
Script para inicializar o banco de dados criando todas as tabelas.
"""
from database.database import engine, Base
from models.f1_models import Driver, Team, Race, Result, Lap, UpdateJob
from models.user import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    """
    Cria todas as tabelas no banco de dados.
    """
    logger.info("Iniciando criação das tabelas no banco de dados...")
    
    try:
        # Cria todas as tabelas definidas nos modelos
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Tabelas criadas com sucesso!")
        
        # Lista as tabelas criadas
        tables = Base.metadata.tables.keys()
        logger.info(f"Tabelas criadas: {', '.join(tables)}")
        
    except Exception as e:
        logger.error(f"✗ Erro ao criar tabelas: {str(e)}")
        raise


if __name__ == "__main__":
    init_db()
