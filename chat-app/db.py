from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import config

database_url = config.DATABASE_URL
engine = create_engine(database_url, echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
