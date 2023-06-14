import sys
sys.path.append("..")

import base64
from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import update

from manage_app.db.database import get_session
from manage_app.models.transport_docs import TransportDocs
from manage_app.models.users import Company, User
from manage_app.schemas.docs_schema import CreateDocs, UpdateDocs


class DocsService:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.db = session

    def create_document(self, docs_data: CreateDocs, user: User) -> dict:
        company_sender = user.company[0].id
        company_receiver = self.db.query(Company).filter(
            Company.company_tax_number==docs_data.company_receiver_tax_code
        ).first()
        new_document = TransportDocs(
            prod_height=docs_data.prod_height,
            prod_length=docs_data.prod_length,
            prod_width=docs_data.prod_width,
            company_sender=company_sender,
            company_receiver=company_receiver.id
        )
        self.db.add(new_document)
        self.db.commit()
        return {"response": f"{new_document} created successful"}

    def get_document(self, document_id: str) -> TransportDocs | dict:
        document = self.db.query(TransportDocs).filter(
            TransportDocs.document_id==document_id
        ).first()
        if not document:
            return {"response": f"No document with ID {document_id}"}
        return self._validation_signature(document=document)

    def get_all_company_documents(
        self,
        user: User
    ) -> List[ TransportDocs | None]:
        return self.db.query(TransportDocs).filter(
            (
                TransportDocs.company_sender==user.company[0].id
            ) | (
                TransportDocs.company_receiver==user.company[0].id
            )
        ).all()

    def delete_document(
        self,
        user: User,
        document_id: str
    ) -> None:
        document = self.db.query(TransportDocs).filter(
            TransportDocs.document_id==document_id,
            TransportDocs.company_sender==user.company[0].id,
            TransportDocs.is_signed==False
        ).first()
        if document:
            self.db.delete(document)
            self.db.commit()

    def update_document(
        self,
        document_id: str,
        documnet_data: UpdateDocs,
        user: User
    ) -> dict:
        document = self.db.query(TransportDocs).filter(
            TransportDocs.document_id==document_id,
            TransportDocs.company_sender==user.company[0].id,
            TransportDocs.is_signed==False
        )
        if not document.first():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don`t have permision for this operation"
            )
        document.update(documnet_data.dict())
        self.db.commit()
        return {"response": f"{document.first()} updated successful"}

    def apply_signature(
        self,
        document_id: str,
        user: User
    ) -> None:
        """
        Create signature from document parameter and company tax number.
        """
        document = self.db.query(TransportDocs).filter(
            TransportDocs.document_id==document_id,
            TransportDocs.is_signed==False,
            (
                TransportDocs.company_sender==user.company[0].id
            ) | (
                TransportDocs.company_receiver==user.company[0].id
            )
        )
        tmp = document.first()
        if not tmp:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don`t have permision for this operation"
            )
        match user.company[0].id:
            case tmp.company_sender:
                signature = self._form_signature(
                    document=tmp, user=user
                )
                document.update({
                    "sender_sign": signature.hex()
                })
                self.db.commit()
            case tmp.company_receiver:
                signature = self._form_signature(
                    document=tmp, user=user
                )
                document.update({
                    "receiver_sign": signature.hex()
                })
                self.db.commit()
        if self._is_both_side_signature(document=document.first()):
            document.update({"is_signed": True})
            self.db.commit()
        return

    def _validation_signature(
        self,
        document: TransportDocs
    ) -> TransportDocs | dict:
        """
        Validate if sender and receiver signatures is correct.
        """
        if document.sender_sign and document.receiver_sign:
            sender = self.db.query(Company).filter(
                Company.id==document.company_sender
            ).first()
            receiver = self.db.query(Company).filter(
                Company.id==document.company_receiver
            ).first()
            sender_sign = self._form_signature(
                document=document, user=sender.director
            )
            receiver_sign = self._form_signature(
                document=document, user=receiver.director
            )
            if document.sender_sign != sender_sign.hex() \
                or document.receiver_sign != receiver_sign.hex():
                return {"response": "Attention document not valid!!!"}
        return document

    @staticmethod
    def _form_signature(document: TransportDocs, user: User) -> str:
        """
        Create encoded signature.
        """
        data = {
            "tax_code": user.company[0].company_tax_number,
            "height": document.prod_height,
            "length": document.prod_length,
            "width": document.prod_width
        }
        sorted_data = sorted(data.items(), key=lambda x: x[0])
        values = map(lambda x: str(x[1]), sorted_data)
        signature = bytes("[+]".join(values), encoding="utf-8")
        return base64.b64encode(signature)

    @staticmethod
    def _is_both_side_signature(document: TransportDocs) -> bool:
        """
        Verify if document was signature by sender and receiver companies.
        """
        d = document
        return d.sender_sign is not None and d.receiver_sign is not None
