import sys
sys.path.append('..')

from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from control_app.db.database import get_session
from control_app.models.users import User
from control_app.schemas.user_schema import CreateUser, UpdateUser
from .utils import PasswordManager


class ControlService:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.db = session

    def create_controller(self, user_data: CreateUser) -> dict:
        new_controller = User(
            username=user_data.username,
            email=user_data.email,
            password=PasswordManager.create_password(
                pswd=user_data.password
            ),
            firstname=user_data.firstname,
            lastname=user_data.lastname,
            org_id=user_data.org_id,
            dep_id=user_data.dep_id,
            role_id=2
        )
        self.db.add(new_controller)
        self.db.commit()
        self.db.refresh(new_controller)
        return {"response": f"{new_controller} created successful"}

    def get_all_controllers(self) -> List[User | None]:
        return self.db.query(User).filter(User.role_id==2).all()

    def get_by_controller_id(self, controller_id: str) -> User | None:
        return self.db.query(User).filter(
            User.user_id==controller_id
        ).first()

    def delete_controller(self, controller_id: str) -> None:
        controller = self.db.query(
            User
        ).filter(User.user_id==controller_id)
        if controller.first():
            controller.delete()
            self.db.commit()
        return

    def update_controller(
        self,
        controller_id: str,
        data: UpdateUser
    ) -> dict:
        controller = self.db.query(
            User
        ).filter(User.user_id==controller_id)
        if not controller.first():
            return {"response": f"No controller with ID {controller_id}"}
        controller.update(data.dict())
        self.db.commit()
        return {"response": f"Controller data was updated successful"}
