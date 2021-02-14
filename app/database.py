from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . import settings

engine = create_engine(str(settings.DATABASE_URL), pool_size=1000, max_overflow=100)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
Base.metadata.bind = engine


def get_session():
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()


get_session_context = contextmanager(get_session)
