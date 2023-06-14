import sys
sys.path.append("..")

from uuid import uuid4

from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from manage_app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    user_id = Column(String(32), default=lambda: uuid4().hex, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)

    company = relationship("Company", back_populates="director")

    def __str__(self):
        return f"<User: {self.username}>"


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer(), primary_key=True)
    company_id = Column(String(32), default=lambda: uuid4().hex, unique=True)
    company_name = Column(Text(), nullable=False)
    company_tax_number = Column(Integer(), nullable=False, unique=True)
    company_email = Column(String(255), nullable=False)
    company_address = Column(Text(), nullable=False)

    director_id = Column(Integer(), ForeignKey("users.id"))
    director = relationship("User", back_populates="company")

    def __str__(self):
        return f"<Company: {self.company_name}>"
