from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

from app.core.oauth2 import OAuth2JWT
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.services.user import UserService

router_user = APIRouter(prefix="/api/v1/users", tags=["users"])
user_service = UserService()


class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    password: str


@router_user.get("/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: int) -> UserOut:
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    return user


@router_user.get("/by-username/{username}", response_model=UserOut)
def get_user_by_username(username: str) -> UserOut:
    user = user_service.get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    return user


@router_user.post("", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(payload: UserCreate) -> UserOut:
    existing = user_service.get_user_by_username(payload.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="username already exists"
        )
    user = User(
        username=payload.username,
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=OAuth2JWT.get_password_hash(payload.password),
        disabled=False,
    )
    user = user_service.create_user(user)
    return user
