from os import get_env
from sqlmodel import create_engine, Session
from dotenv import load_dotenv

load_dotenv()

# Read database URL from .env
SQLMODEL_DATABASE_URI = get_env("DATABASE_URL", "sqlite:///random_books.db")

# Create database-engine
engine = create_engine(SQLMODEL_DATABASE_URI, echo=True)


# Dependency to get a database session for the endpoints
def get_session():
    with Session(engine) as session:
        yield session
