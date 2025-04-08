from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from models import *  # Import all models so Base knows about them


SQLALCHEMY_DATABASE_URL = "sqlite:///./RGSoD.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def init_db():
 
    Base.metadata.create_all(bind=engine)
