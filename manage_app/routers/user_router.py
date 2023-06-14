import sys
sys.path.append("..")

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from manage_app.schemas.user_schema import CreateUser
from manage_app.services.auth_service import AuthService
from manage_app.services.sign_up_service import SignUpService


router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


@router.post("/sign-up/", status_code=status.HTTP_201_CREATED)
def sign_up(
    user_data: CreateUser,
    service: SignUpService = Depends()
):
    return service.sign_up(user_data=user_data)


@router.post("/sign-in/")
def sign_in(
    user_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends()
):
    return service.authentication(
        username=user_data.username, password=user_data.password
    )
