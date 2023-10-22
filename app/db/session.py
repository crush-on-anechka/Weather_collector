import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append('/app')

from settings import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
