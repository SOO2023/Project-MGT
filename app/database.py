from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("DB_URL")
engine = create_engine(url=URL)
sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


class Base(DeclarativeBase):
    pass


def db_session():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()
