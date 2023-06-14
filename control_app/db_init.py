from os import getcwd
from os.path import join, isfile

from passlib.hash import bcrypt

from settings import settings
from db.database import Base, engine, session
from models.organizations import *
from models.users import *


def init_db():
    Base.metadata.create_all(engine)
    db = session()
    admin = Role(role_name="admin")
    user = Role(role_name="controller")
    db.add_all([admin, user])
    db.commit()
    su = User(
        username=settings.ADMIN_NAME,
        password=bcrypt.hash(settings.ADMIN_PASSWORD),
        email="transport_doc_app_admin@mail.com",
        firstname="John",
        lastname="Doe",
        role_id=1
    )
    db.add(su)
    db.commit()
    db.close()


if __name__ == "__main__":
    db_name = settings.DB_URL.split(':///')[-1]
    db_file_path = join(getcwd(), db_name)
    if not isfile(db_file_path):
        init_db()
