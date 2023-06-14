import sys
sys.path.append('..')

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from control_app.models.users import User
from control_app.services.auth_service import AuthService
from control_app.routers.utils import get_user


router = APIRouter(
    prefix='/auth',
    tags=["User Authentication"]
)


@router.post('/sign-in')
def sign_in(
    user_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends()
):
    return service.authentication(
        username=user_data.username,
        password=user_data.password
    )
