import sys
sys.path.append("..")

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from control_app.settings import settings


engine = create_engine(
    url=settings.DB_URL, connect_args={"check_same_thread": False}
)

session = sessionmaker(
    autoflush=False, autocommit=False, bind=engine
)

Base = declarative_base()


def get_session() -> Session:
    db = session()
    try:
        yield db
    finally:
        db.close()
