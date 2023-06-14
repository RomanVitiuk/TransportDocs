import sys
sys.path.append("..")

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from manage_app.services.auth_service import AuthService


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/user/sign-in/")


def get_user(
    token: str = Depends(oauth2_schema)
):
    return AuthService.verify_token(token=token)
