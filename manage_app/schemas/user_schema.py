from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    firstname: str
    lastname: str


class CreateUser(BaseUser):
    password: str


class ReadUser(BaseUser):
    user_id: str

    class Config:
        orm_mode = True
