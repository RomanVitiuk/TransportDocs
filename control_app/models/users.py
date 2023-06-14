import sys
sys.path.append("..")

from uuid import uuid4

from sqlalchemy import (
    Column, Integer, ForeignKey,
    String, Text
)
from sqlalchemy.orm import relationship

from control_app.db.database import Base


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer(), primary_key=True)
    role_name = Column(String(20), nullable=False)

    def __str__(self):
        return f"Role {self.role_name}"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    user_id = Column(String(32), default=lambda: uuid4().hex, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(32), nullable=False)
    email = Column(String(255), nullable=False)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)

    org_id = Column(
        Integer(),
        ForeignKey('organizations.org_id'),
        nullable=True
    )
    organization = relationship("Organization", back_populates="user")

    dep_id = Column(
        Integer(),
        ForeignKey("departments.dep_id"),
        nullable=True
    )
    department = relationship("Department", back_populates="user")

    role_id = Column(Integer(), ForeignKey("roles.role_id"))

    def __str__(self):
        return f"Person {self.firstname} {self.lastname}"


# user_id = "f79e0ff1f5234787bcf4002a0620e7bf"
# username = superuser_su
# password = password
