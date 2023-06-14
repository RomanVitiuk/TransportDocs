import sys
sys.path.append("..")

from fastapi import APIRouter, Depends, HTTPException, status

from control_app.services.auth_service import AuthService
from control_app.services.check_docs_service import DocsService
from .utils import get_user, PermissionRole


router = APIRouter(
    prefix="/docs-controle",
    tags=["Check Transport Documents"]
)


@router.get("/{invoice_id}/")
def get_docs_info(
    invoice_id: str,
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    docs_service: DocsService = Depends()
):
    role = auth_service.autorization(user_id=user_id)
    match role:
        case PermissionRole.controller.value:
            return docs_service.get_docs_info(
                invoice_id=invoice_id
            )
        case PermissionRole.admin.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don`t have permission for this operation"
            )
