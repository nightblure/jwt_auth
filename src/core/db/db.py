from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_sessionmaker(db_url):
    engine = create_engine(
        db_url,
        pool_size=20,
        max_overflow=0,
        pool_pre_ping=False
    )
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
