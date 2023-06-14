import sys
sys.path.append("..")

from fastapi import Depends
from sqlalchemy.orm import Session

from manage_app.db.database import get_session
from manage_app.models.users import User
from manage_app.schemas.user_schema import CreateUser
from .utils import PasswordManager


class SignUpService:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.db = session

    def sign_up(self, user_data: CreateUser) -> dict:
        new_user = User(
            username=user_data.username,
            password=PasswordManager.create_password(
                pswd=user_data.password
            ),
            email=user_data.email,
            firstname=user_data.firstname,
            lastname=user_data.lastname
        )
        self.db.add(new_user)
        self.db.commit()
        return {"response": f"{new_user} created successful"}
