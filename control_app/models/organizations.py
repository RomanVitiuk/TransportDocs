import sys
sys.path.append("..")

from sqlalchemy import (
    Column, Integer, ForeignKey,
    String, Text
)
from sqlalchemy.orm import relationship

from control_app.db.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    org_id = Column(Integer(), primary_key=True)
    org_name = Column(Text(), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    address = Column(Text(), nullable=False)

    user = relationship("User", back_populates="organization")

    def __str__(self):
        return f"Organization: {self.org_name}"


class Department(Base):
    __tablename__ = "departments"

    dep_id = Column(Integer(), primary_key=True)
    dep_name = Column(Text(), nullable=False)

    org_id = Column(Integer(), ForeignKey("organizations.org_id"))

    user = relationship("User", back_populates="department")

    def __str__(self):
        return f"Departmane: {self.dep_name}"
