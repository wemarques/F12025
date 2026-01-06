"""
Modelos SQLAlchemy para dados da Fórmula 1.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime


class Driver(Base):
    """Modelo para pilotos da F1."""
    __tablename__ = "drivers"
    
    id = Column(Integer, primary_key=True, index=True)
    abbreviation = Column(String(3), unique=True, index=True, nullable=False)  # Ex: VER, HAM
    full_name = Column(String(100), nullable=False)
    number = Column(Integer, nullable=True)
    team_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    results = relationship("Result", back_populates="driver")
    laps = relationship("Lap", back_populates="driver")
    
    def __repr__(self):
        return f"<Driver {self.abbreviation}: {self.full_name}>"


class Team(Base):
    """Modelo para equipes/construtores da F1."""
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    results = relationship("Result", back_populates="team")
    
    def __repr__(self):
        return f"<Team {self.name}>"


class Race(Base):
    """Modelo para corridas da F1."""
    __tablename__ = "races"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, index=True)
    round_number = Column(Integer, nullable=False)
    event_name = Column(String(200), nullable=False)
    location = Column(String(200), nullable=True)
    country = Column(String(100), nullable=True)
    event_date = Column(DateTime, nullable=True)
    event_format = Column(String(50), nullable=True)  # conventional, sprint, etc.
    circuit_name = Column(String(200), nullable=True)
    
    # Metadados da sessão
    session_type = Column(String(20), nullable=True)  # R (Race), Q (Qualifying), FP1, etc.
    total_laps = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    results = relationship("Result", back_populates="race", cascade="all, delete-orphan")
    laps = relationship("Lap", back_populates="race", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Race {self.year} R{self.round_number}: {self.event_name}>"


class Result(Base):
    """Modelo para resultados de pilotos em corridas."""
    __tablename__ = "results"
    
    id = Column(Integer, primary_key=True, index=True)
    race_id = Column(Integer, ForeignKey("races.id", ondelete="CASCADE"), nullable=False, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    
    # Dados de resultado
    position = Column(Integer, nullable=True)  # Posição final
    grid_position = Column(Integer, nullable=True)  # Posição no grid de largada
    points = Column(Float, nullable=True)
    status = Column(String(50), nullable=True)  # Finished, DNF, etc.
    time = Column(String(50), nullable=True)  # Tempo total da corrida
    fastest_lap = Column(String(50), nullable=True)
    fastest_lap_rank = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    race = relationship("Race", back_populates="results")
    driver = relationship("Driver", back_populates="results")
    team = relationship("Team", back_populates="results")
    
    def __repr__(self):
        return f"<Result Race#{self.race_id} Driver#{self.driver_id} P{self.position}>"


class Lap(Base):
    """Modelo para dados de voltas individuais."""
    __tablename__ = "laps"
    
    id = Column(Integer, primary_key=True, index=True)
    race_id = Column(Integer, ForeignKey("races.id", ondelete="CASCADE"), nullable=False, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False, index=True)
    
    # Dados da volta
    lap_number = Column(Integer, nullable=False)
    lap_time = Column(Float, nullable=True)  # Tempo em segundos
    lap_time_str = Column(String(20), nullable=True)  # Tempo formatado (ex: "1:23.456")
    sector_1_time = Column(Float, nullable=True)
    sector_2_time = Column(Float, nullable=True)
    sector_3_time = Column(Float, nullable=True)
    
    # Dados adicionais
    speed_i1 = Column(Float, nullable=True)  # Velocidade no speed trap 1
    speed_i2 = Column(Float, nullable=True)  # Velocidade no speed trap 2
    speed_fl = Column(Float, nullable=True)  # Velocidade na linha de chegada
    speed_st = Column(Float, nullable=True)  # Velocidade no speed trap
    
    # Flags e status
    is_personal_best = Column(Boolean, default=False)
    is_accurate = Column(Boolean, default=True)
    pit_out_time = Column(Float, nullable=True)
    pit_in_time = Column(Float, nullable=True)
    
    # Posição na volta
    position = Column(Integer, nullable=True)
    
    # Compound do pneu
    compound = Column(String(20), nullable=True)  # SOFT, MEDIUM, HARD, etc.
    tyre_life = Column(Integer, nullable=True)  # Idade do pneu em voltas
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    race = relationship("Race", back_populates="laps")
    driver = relationship("Driver", back_populates="laps")
    
    def __repr__(self):
        return f"<Lap Race#{self.race_id} Driver#{self.driver_id} Lap#{self.lap_number}>"


class UpdateJob(Base):
    """Modelo para rastrear jobs de atualização de dados."""
    __tablename__ = "update_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, index=True)
    status = Column(String(20), nullable=False, default="running")  # running, completed, failed
    events_processed = Column(Integer, default=0)
    events_failed = Column(Integer, default=0)
    total_events = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<UpdateJob {self.year} - {self.status}>"
