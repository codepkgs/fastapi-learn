import datetime

import jwt
from fastapi import HTTPException, status
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from app.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()


class OAuth2JWT:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(
        data: dict, expires_delta: datetime.timedelta | None = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.now(datetime.UTC) + expires_delta
        else:
            expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
                minutes=settings.oauth2.access_token_expire_minutes
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            payload=to_encode,
            key=settings.oauth2.secret_key,
            algorithm=settings.oauth2.algorithm,
        )
        return encoded_jwt

    @staticmethod
    def get_current_user(token: str):
        try:
            payload = jwt.decode(
                jwt=token,
                key=settings.oauth2.secret_key,
                algorithms=[settings.oauth2.algorithm],
            )
            # 从sub中获取username
            username = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return username
        except InvalidTokenError as err:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not validate credentials, {str(err)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
