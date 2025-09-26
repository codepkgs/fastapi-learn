import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.core.config import get_settings
from app.core.oauth2 import OAuth2JWT
from app.schemas.oauth2 import TokenResponse

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


@router_auth.post("/token", response_model=TokenResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
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


@router_auth.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    current_user = OAuth2JWT.get_current_user(token)
    return {"message": f"Hello, {current_user}. This is a protected route."}
