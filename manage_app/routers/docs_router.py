import sys
sys.path.append("..")

from typing import List

from fastapi import APIRouter, Depends, status

from manage_app.schemas.docs_schema import (
    CreateDocs, ReadDocs, UpdateDocs
)
from manage_app.services.auth_service import AuthService
from manage_app.services.docs_service import DocsService
from .utils import get_user


router = APIRouter(
    prefix="/document",
    tags=["Transport Documents"]
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def create_document(
    docs_data: CreateDocs,
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    docs_service: DocsService = Depends()
):
    user = auth_service.get_current_user(user_id=user_id)
    return docs_service.create_document(
        docs_data=docs_data, user=user
    )


@router.get(
    "/{document_id}/",
    response_model=ReadDocs | dict,
    status_code=status.HTTP_200_OK
)
def get_document(
    document_id: str,
    docs_service: DocsService = Depends()
):
    return docs_service.get_document(document_id=document_id)


@router.get(
    "/",
    response_model=List[ReadDocs] | None,
    status_code=status.HTTP_200_OK
)
def get_all_company_documents(
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    docs_service: DocsService = Depends()
):
    user = auth_service.get_current_user(user_id=user_id)
    return docs_service.get_all_company_documents(
        user=user
    )


@router.delete(
    "/{document_id}/",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_document(
    document_id: str,
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    docs_service: DocsService = Depends()
):
    user = auth_service.get_current_user(user_id=user_id)
    return docs_service.delete_document(
        user=user, document_id=document_id
    )


@router.patch(
    "/{document_id}/"
)
def update_document(
    document_id: str,
    document_data: UpdateDocs,
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    docs_service: DocsService = Depends()
):
    user = auth_service.get_current_user(user_id=user_id)
    return docs_service.update_document(
        document_id=document_id,
        documnet_data=document_data,
        user=user
    )


@router.patch("/signature/{document_id}/")
def apply_signature(
    document_id: str,
    user_id: str = Depends(get_user),
    auth_service: AuthService = Depends(),
    docs_service: DocsService = Depends()
):
    user = auth_service.get_current_user(user_id=user_id)
    docs_service.apply_signature(
        document_id=document_id, user=user
    )
    return {"response": f"{user} successful aplly signature"}
