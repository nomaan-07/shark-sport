from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, joinedload, join, relationship
from sqlalchemy.ext.declarative import declarative_base
import os, dotenv

dotenv.load_dotenv()

DB_PASS = os.getenv("DB_PASSWORD")
DB_USER_NAME =  os.getenv("DB_USER_NAME")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
"""DATABASE_URL= f"postgresql://postgres:DB_PASS@host.docker.internal:5432/sharksport""" # use for container 
DATABASE_URL = f"postgresql://{DB_USER_NAME}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind = engine, autoflush = False, autocommit = False)

Base = declarative_base()




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


