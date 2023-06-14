import sys
sys.path.append("..")

from fastapi import APIRouter, Depends, status

from manage_app.schemas.company_schema import CreateCompany, UpdateCompany
from manage_app.services.auth_service import AuthService
from manage_app.services.company_service import CompanyService
from .utils import get_user


router = APIRouter(
    prefix="/company",
    tags=["Company"]
)


@router.post("/")
def create_company(
    company_data: CreateCompany,
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    company_service: CompanyService = Depends()
):
    user = auth_service.get_current_user(user_id=user_id)
    return company_service.create_company(
        company_data=company_data, id=user.id
    )


@router.get("/")
def get_company(
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    company_service: CompanyService = Depends()
):
    user = auth_service.get_current_user(user_id=user_id)
    return company_service.get_company(id=user.id)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    company_service: CompanyService = Depends()
):
    user = auth_service.get_current_user(user_id=user_id)
    company_service.delete_company(id=user.id)


@router.patch("/")
def update_company(
    company_data: UpdateCompany,
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    company_service: CompanyService = Depends()
):
    user = auth_service.get_current_user(user_id=user_id)
    return company_service.update_company(
        id=user.id, company_data=company_data
    )
