from os import getcwd
from os.path import join, isfile

from db.database import Base, engine, session
from models.transport_docs import *
from models.users import *
from settings import settings


def init_db():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    db_name = settings.DB_URL.split(':///')[-1]
    db_file_path = join(getcwd(), db_name)
    if not isfile(db_file_path):
        init_db()
