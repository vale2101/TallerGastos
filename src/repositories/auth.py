from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.repositories.user import UserRepository
from src.config.database import SessionLocal
from src.auth.jwt_handler import JWTHandler
from src.schemas.user import UserLogin as UserLoginSchema, UserCreate as UserCreateSchema
from src.config.security import auth_secret_key, auth_algorithm

jwt_handler = JWTHandler(auth_secret_key, auth_algorithm)

class AuthRepository:
    def __init__(self) -> None:
        pass

    def register_user(self, user: UserCreateSchema) -> dict:
        db: Session = SessionLocal()
        user_repo = UserRepository(db)

        if user_repo.get_user_by_email(user.email) is not None:
            raise Exception("Account already exists")

        hashed_password = jwt_handler.hash_password(user.password)
        new_user = user_repo.create_user(UserCreateSchema(name=user.name, email=user.email, password=hashed_password))
        return new_user

    def login_user(self, user: UserLoginSchema) -> dict:
        db: Session = SessionLocal()
        user_repo = UserRepository(db)
        check_user = user_repo.get_user_by_email(user.email)

        if check_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials (1)")
        if not check_user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The user is not allowed to log in")
        if not jwt_handler.verify_password(user.password, check_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials (2)")

        access_token = jwt_handler.encode_token(check_user)
        refresh_token = jwt_handler.encode_refresh_token(check_user)
        return access_token, refresh_token
