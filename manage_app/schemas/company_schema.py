from pydantic import BaseModel, EmailStr


class BaseCompany(BaseModel):
    company_name: str
    company_tax_number: int
    company_email: EmailStr
    company_address: str


class CreateCompany(BaseCompany):
    pass


class UpdateCompany(BaseModel):
    company_name: str
    company_email: EmailStr
    company_address: str


class ReadCompany(BaseCompany):
    company_id: str

    class Config:
        orm_mode = True
