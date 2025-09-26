import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from loguru import logger

from app.core.config import get_settings
from app.core.oauth2 import OAuth2JWT
from app.schemas.oauth2 import LoginRequest, TokenResponse

settings = get_settings()
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$AKHYe/6lkn28X29L1QRfZujbqX4PL9dVJB5odXatw5zknD48yLNSe",
        "disabled": False,
    }
}
router_auth = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 使用OAuth2PasswordRequestForm获取token - Form请求体
@router_auth.post("/token", response_model=TokenResponse)
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = fake_users_db.get(form_data.username)
    if not user or not OAuth2JWT.verify_password(
        form_data.password, user["hashed_password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = OAuth2JWT.create_access_token(
        data={"sub": user["username"]},
        expires_delta=datetime.timedelta(
            minutes=settings.oauth2.access_token_expire_minutes
        ),
    )
    return TokenResponse(access_token=access_token, token_type="bearer")


# 使用LoginRequest获取token - JSON请求体
@router_auth.post("/login", response_model=TokenResponse)
async def login(login: LoginRequest):
    user = fake_users_db.get(login.username)
    if not user or not OAuth2JWT.verify_password(
        login.password, user["hashed_password"]
    ):
        logger.error(
            f"User {login.username} is logging in with invalid username or password"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = OAuth2JWT.create_access_token(
        data={"sub": user["username"]},
        expires_delta=datetime.timedelta(
            minutes=settings.oauth2.access_token_expire_minutes
        ),
    )
    logger.success(f"User {user['username']} is logging in")

    return TokenResponse(access_token=access_token, token_type="bearer")
