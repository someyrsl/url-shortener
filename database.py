from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://app:secret@localhost:5432/urlshortener"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()