from pydantic import BaseModel, EmailStr


class BaseOrganization(BaseModel):
    org_name: str
    email: EmailStr
    address: str


class CreateOrganization(BaseOrganization):
    pass


class UpdateOrganization(BaseOrganization):
    pass


class ReadOrganization(BaseOrganization):
    org_id: int

    class Config:
        orm_mode = True


class BaseDepartment(BaseModel):
    dep_name: str


class CreateDepartment(BaseDepartment):
    org_id: int


class UpdateDepartment(CreateDepartment):
    pass


class ReadDepartment(CreateDepartment):
    dep_id: int

    class Config:
        orm_mode = True
