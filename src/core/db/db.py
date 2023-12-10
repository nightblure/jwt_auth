from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.db_url,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
