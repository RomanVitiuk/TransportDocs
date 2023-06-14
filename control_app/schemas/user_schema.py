from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    firstname: str
    lastname: str


class CreateUser(BaseUser):
    password: str
    org_id: int
    dep_id: int


class UpdateUser(BaseUser):
    org_id: int
    dep_id: int


class ReadUser(BaseUser):
    user_id: str

    class Config:
        orm_mode = True
