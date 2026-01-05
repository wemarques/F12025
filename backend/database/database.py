import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Prioriza a DATABASE_URL do ambiente (produção), senão usa SQLite (local)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./f1fantasy.db")

# Adiciona configuração específica para PostgreSQL
if DATABASE_URL.startswith("postgres"):
    engine = create_engine(DATABASE_URL)
else:
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
