import sys
sys.path.append("..")

from fastapi import Depends
from sqlalchemy.orm import Session

from manage_app.db.database import get_session
from manage_app.models.users import Company
from manage_app.schemas.company_schema import CreateCompany, UpdateCompany


class CompanyService:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.db = session

    def create_company(self, company_data: CreateCompany, id: int) -> dict:
        new_company = Company(**company_data.dict())
        new_company.director_id = id
        self.db.add(new_company)
        self.db.commit()
        return {"response": f"{new_company} created successful!"}

    def get_company(self, id: int) -> Company | None:
        return self.db.query(
            Company
        ).filter(Company.director_id==id).first()

    def delete_company(self, id: int) -> None:
        company = self.db.query(
            Company
        ).filter(Company.director_id==id)
        if company.first():
            company.delete()
            self.db.commit()
        return

    def update_company(self, id: int, company_data: UpdateCompany) -> dict:
        company = self.db.query(Company).filter(
            Company.director_id==id
        )
        if not company.first():
            return {"response": f"You aren`t have any company in our system yet!"}
        company.update(company_data.dict())
        self.db.commit()
        return {"response": "Company info updated successful!"}
