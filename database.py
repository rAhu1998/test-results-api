import os
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

database_url = os.getenv("DATABASE_URL")
if database_url is None:
    raise RuntimeError("DATABASE_URL is not set, check .env")
engine = sqlalchemy.create_engine(database_url)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
