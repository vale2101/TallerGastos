from typing import List
from src.schemas.user import User as UserSchema, UserCreate as UserCreateSchema
from src.models.user import UserModel

class UserRepository:
    def __init__(self, db):
        self.db = db

    def get_user_by_id(self, id: int) -> UserSchema:
        element = self.db.query(UserModel).filter(UserModel.id == id).first()
        return element

    def get_user_by_email(self, email: str) -> UserSchema:
        element = self.db.query(UserModel).filter(UserModel.email == email).first()
        return element

    def create_user(self, user: UserCreateSchema) -> UserModel:
        new_user = UserModel(**user.model_dump())
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
