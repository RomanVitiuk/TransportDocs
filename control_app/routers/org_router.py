import sys
sys.path.append("..")

from fastapi import APIRouter, Depends, HTTPException, status

from control_app.models.organizations import Department, Organization
from control_app.schemas.organization_schema import (
    CreateOrganization, CreateDepartment,
    UpdateOrganization, UpdateDepartment
)
from control_app.services.auth_service import AuthService
from control_app.services.organization_service import OrgService
from .utils import get_user, PermissionRole


router = APIRouter(
    prefix='/organization',
    tags=["Control Organizations"]
)

# --------------- ORGANIZATION BLOCK ------------------------

@router.post("/")
def create_organization(
    org_data: CreateOrganization,
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    org_service: OrgService = Depends()
):
    role = auth_service.autorization(user_id=user_id)
    match role:
        case PermissionRole.admin.value:
            return org_service.create_organization(org_data=org_data)
        case PermissionRole.controller.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don`t have permission for this operation"
            )


@router.get("/{org_id}/")
def get_organization_by_id(
    org_id: int,
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    org_service: OrgService = Depends()
):
    role = auth_service.autorization(user_id=user_id)
    match role:
        case PermissionRole.admin.value:
            return org_service.get_organization_by_id(org_id=org_id)
        case PermissionRole.controller.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don`t have permission for this operation"
            )


@router.get("/")
def get_all_organization(
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    org_service: OrgService = Depends()
):
    role = auth_service.autorization(user_id=user_id)
    match role:
        case PermissionRole.admin.value:
            return org_service.get_all_organization()
        case PermissionRole.controller.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don`t have permission for this operation"
            )


@router.patch("/{org_id}/")
def update_organization(
    org_id: int,
    org_data: UpdateOrganization,
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    org_service: OrgService = Depends()
):
    role = auth_service.autorization(user_id=user_id)
    match role:
        case PermissionRole.admin.value:
            return org_service.update_organization(
                org_id=org_id, org_data=org_data
            )
        case PermissionRole.controller.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don`t have permission for this operation"
            )


@router.delete("/{org_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_organization(
    org_id: int,
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    org_service: OrgService = Depends()
):
    role = auth_service.autorization(user_id=user_id)
    match role:
        case PermissionRole.admin.value:
            return org_service.delete_organization(org_id=org_id)
        case PermissionRole.controller.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don`t have permission for this operation"
            )

# --------------- DEPARTMENT BLOCK ------------------------

@router.post("/department/")
def create_department(
    dep_data: CreateDepartment,
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    dep_service: OrgService = Depends()
):
    role = auth_service.autorization(user_id=user_id)
    match role:
        case PermissionRole.admin.value:
            return dep_service.create_department(dep_data=dep_data)
        case PermissionRole.controller.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don`t have permission for this operation"
            )


@router.get("/department/{dep_id}/")
def get_department_by_id(
    dep_id: int,
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    dep_service: OrgService = Depends()
):
    role = auth_service.autorization(user_id=user_id)
    match role:
        case PermissionRole.admin.value:
            return dep_service.get_department_by_id(dep_id=dep_id)
        case PermissionRole.controller.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don`t have permission for this operation"
            )


@router.get("/department")
def get_all_department(
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    dep_service: OrgService = Depends()
):
    role = auth_service.autorization(user_id=user_id)
    match role:
        case PermissionRole.admin.value:
            return dep_service.get_all_department()
        case PermissionRole.controller.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don`t have permission for this operation"
            )


@router.patch("/department/{dep_id}/")
def update_department(
    dep_id: int,
    data: UpdateDepartment,
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    dep_service: OrgService = Depends()
):
    role = auth_service.autorization(user_id=user_id)
    match role:
        case PermissionRole.admin.value:
            return dep_service.update_department(
                dep_id=dep_id, data=data
            )
        case PermissionRole.controller.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don`t have permission for this operation"
            )


@router.delete(
    "/department/{dep_id}/", status_code=status.HTTP_204_NO_CONTENT
)
def delete_department(
    dep_id: int,
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    dep_service: OrgService = Depends()
):
    role = auth_service.autorization(user_id=user_id)
    match role:
        case PermissionRole.admin.value:
            return dep_service.delete_department(dep_id=dep_id)
        case PermissionRole.controller.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don`t have permission for this operation"
            )
