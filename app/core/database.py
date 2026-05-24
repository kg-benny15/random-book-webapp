from os import getenv
from sqlmodel import create_engine, Session, text
from dotenv import load_dotenv

load_dotenv()


def get_engine(env_database_key: str = "DATABASE_URL", echo_value: bool = True):
    # Read database URL from .env
    sqlmodel_database_uri = getenv(env_database_key, "sqlite:///random_books.db")
    # Create database-engine
    return create_engine(sqlmodel_database_uri, echo=echo_value)


# Production/Development Engine
engine = get_engine()
# Test Engine
test_engine = get_engine(env_database_key="TEST_DATABASE_URL", echo_value=False)


# Dependency to get a database session for the endpoints
def get_session(testing: bool = False):
    if not testing:
        with Session(engine) as session:
            yield session
    else:
        with Session(test_engine) as test_session:
            try:
                test_session.exec(text("PRAGMA foreign_keys = ON"))
                yield test_session
            finally:
                test_session.rollback()
