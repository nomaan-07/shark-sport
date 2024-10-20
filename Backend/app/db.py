from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, joinedload, join, relationship
from sqlalchemy.ext.declarative import declarative_base
import os, dotenv

dotenv.load_dotenv()

DB_PASS = os.getenv("DB_PASSWORD")

DATABASE_URL= "postgresql://postgres:1050@host.docker.internal:5432/sharksport"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind = engine, autoflush = False, autocommit = False)

Base = declarative_base()




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


