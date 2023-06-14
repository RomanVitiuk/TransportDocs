import sys
sys.path.append("..")

from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from jose import jwt, JWSError
from sqlalchemy.orm import Session

from manage_app.db.database import get_session
from manage_app.models.users import User
from manage_app.schemas.token import Token
from manage_app.settings import settings
from .utils import PasswordManager


class AuthService:
    auth_exep = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    credentials_exep = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.db = session

    @classmethod
    def create_token(cls, user_id: str) -> Token:
        time_now = datetime.utcnow()
        payload = {
            "iat": time_now,
            "nbf": time_now,
            "exp": time_now + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE
            ),
            "sub": str(user_id)
        }
        token = jwt.encode(
            claims=payload,
            key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return Token(access_token=token)

    @classmethod
    def verify_token(cls, token: str) -> str:
        try:
            data = jwt.decode(
                token=token,
                key=settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            user_id = data.get("sub")
            return user_id
        except JWSError:
            raise self.credentials_exep

    def authentication(self, username: str, password: str) -> Token:
        user = self.db.query(User).filter(User.username==username).first()
        if not user:
            raise self.auth_exep
        if not PasswordManager.verify_password(password, user.password):
            raise self.auth_exep
        return self.create_token(user_id=user.user_id)

    def get_current_user(self, user_id: str) -> User:
        return self.db.query(User).filter(User.user_id==user_id).first()
