import sys
sys.path.append('..')

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from control_app.models.users import User
from control_app.schemas.user_schema import CreateUser, ReadUser, UpdateUser
from control_app.services.auth_service import AuthService
from control_app.services.control_service import ControlService
from .utils import get_user, PermissionRole


router = APIRouter(
    prefix='/controller',
    tags=["Controller Person"]
)


@router.post("/")
def create_controller(
    user_data: CreateUser,
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    control_service: ControlService = Depends()
):
    role = auth_service.autorization(user_id=user_id)
    match role:
        case PermissionRole.admin.value:
            return control_service.create_controller(user_data=user_data)
        case PermissionRole.controller.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don`t have permission for this operation"
            )


@router.get("/", response_model=List[ReadUser] | None)
def get_all_controllers(
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    control_service: ControlService = Depends()
):
    role = auth_service.autorization(user_id=user_id)
    match role:
        case PermissionRole.admin.value:
            return control_service.get_all_controllers()
        case PermissionRole.controller.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don`t have permission for this operation"
            )


@router.get("/{controller_id}/", response_model=ReadUser | None)
def get_by_controller_id(
    controller_id: str,
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    control_service: ControlService = Depends()
):
    role = auth_service.autorization(user_id=user_id)
    match role:
        case PermissionRole.admin.value:
            return control_service.get_by_controller_id(
                controller_id=controller_id
            )
        case PermissionRole.controller.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don`t have permission for this operation"
            )


@router.delete("/{controller_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_controller(
    controller_id: str,
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    control_service: ControlService = Depends()
):
    role = auth_service.autorization(user_id=user_id)
    match role:
        case PermissionRole.admin.value:
            return control_service.delete_controller(
                controller_id=controller_id
            )
        case PermissionRole.controller.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don`t have permission for this operation"
            )


@router.patch("/{controller_id}/")
def update_controller(
    controller_id: str,
    data: UpdateUser,
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    control_service: ControlService = Depends()
):
    role = auth_service.autorization(user_id=user_id)
    match role:
        case PermissionRole.admin.value:
            return control_service.update_controller(
                controller_id=controller_id,
                data=data
            )
        case PermissionRole.controller.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don`t have permission for this operation"
            )
