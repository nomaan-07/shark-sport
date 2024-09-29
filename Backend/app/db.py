from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base




SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1050@localhost:5432/sharksport"

engine = create_engine(url= SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind = engine, autoflush = False, autocommit = False)

Base = declarative_base()




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


