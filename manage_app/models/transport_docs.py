import sys
sys.path.append("..")

from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Boolean, Column, DateTime, Integer,
    ForeignKey, func, Numeric, String, Text
)
from sqlalchemy.orm import relationship

from manage_app.db.database import Base


class TransportDocs(Base):
    __tablename__ = "documents"

    id = Column(Integer(), primary_key=True)
    document_id = Column(String(32), default=lambda: uuid4().hex, unique=True)
    is_signed = Column(Boolean(), default=False)
    time_created = Column(DateTime(), default=datetime.utcnow())
    prod_length = Column(Numeric(4, 2, asdecimal=False))
    prod_width = Column(Numeric(3, 2, asdecimal=False))
    prod_height = Column(Numeric(3, 2, asdecimal=False))

    sender_sign = Column(String(255), nullable=True)
    receiver_sign = Column(String(255), nullable=True)

    company_sender = Column(Integer(), ForeignKey("companies.id"))
    company_receiver = Column(Integer(), ForeignKey("companies.id"))

    def __str__(self):
        return f"<Transport Document {self.document_id}>"
