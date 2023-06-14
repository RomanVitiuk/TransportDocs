import sys
sys.path.append("..")

from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from control_app.db.database import get_session
from control_app.models.organizations import Department, Organization
from control_app.schemas.organization_schema import (
    CreateOrganization, CreateDepartment,
    UpdateOrganization, UpdateDepartment
)


class OrgService:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.db = session

# --------------- ORGANIZATION BLOCK ------------------------

    def create_organization(self, org_data: CreateOrganization) -> dict:
        new_org = Organization(**org_data.dict())
        self.db.add(new_org)
        self.db.commit()
        self.db.refresh(new_org)
        return {"response": f"{new_org} created successful"}

    def get_organization_by_id(self, org_id: int) -> Organization | None:
        return self.db.query(
            Organization
        ).filter(Organization.org_id==org_id).first()

    def get_all_organization(self) -> List[Organization | None]:
        return self.db.query(Organization).all()

    def update_organization(
        self, org_id: int, org_data: UpdateOrganization
    ) -> dict:
        org = self.db.query(
            Organization
        ).filter(Organization.org_id==org_id)
        if not org.first():
            return {"response": f"No organization with id {org_id}"}
        org.update(org_data.dict())
        self.db.commit()
        return {"response": "Organization updated successful"}

    def delete_organization(self, org_id: int) -> None:
        org = self.db.query(
            Organization
        ).filter(Organization.org_id==org_id)
        if org.first():
            org.delete()
            self.db.commit()
        return

# --------------- DEPARTMENT BLOCK ------------------------

    def create_department(self, dep_data: CreateDepartment) -> dict:
        new_dep = Department(**dep_data.dict())
        self.db.add(new_dep)
        self.db.commit()
        self.db.refresh(new_dep)
        return {"response": f"{new_dep} created successful"}

    def get_department_by_id(self, dep_id: int) -> Department | None:
        return self.db.query(
            Department
        ).filter(Department.dep_id==dep_id).first()

    def get_all_department(self) -> List[Department | None]:
        return self.db.query(Department).all()

    def update_department(self, dep_id: int, data: UpdateDepartment) -> dict:
        dep = self.db.query(
            Department
        ).filter(Department.dep_id==dep_id)
        if not dep.first():
            return {"response": f"No department with ID {dep_id}"}
        dep.update(data.dict())
        self.db.commit()
        return {"response": "Department updated successful"}

    def delete_department(self, dep_id: int) -> None:
        dep = self.db.query(
            Department
        ).filter(Department.dep_id==dep_id)
        if dep.first():
            dep.delete()
            self.db.commit()
        return
