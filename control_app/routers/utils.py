import sys
sys.path.append("..")

from enum import Enum

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from control_app.services.auth_service import AuthService


class PermissionRole(Enum):
    admin = 1
    controller = 2


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/sign-in")


def get_user(
    token: str = Depends(oauth2_schema)
):
    return AuthService.verify_token(token=token)
