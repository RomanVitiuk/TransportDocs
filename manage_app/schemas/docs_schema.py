from datetime import datetime

from pydantic import BaseModel


class BaseDocs(BaseModel):
    prod_length: float
    prod_width: float
    prod_height: float


class CreateDocs(BaseDocs):
    company_receiver_tax_code: int


class UpdateDocs(BaseDocs):
    pass


class ReadDocs(BaseDocs):
    document_id: str
    is_signed: bool
    time_created: datetime
    sender_sign: str | None
    receiver_sign: str | None
    company_sender: int
    company_receiver: int

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }
