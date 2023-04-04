import os
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from dependecies.database import get_repository
from schemas.user import UserAuthentication
from schemas.auth import TokenData
from repository.user import UserRepository
from services.auth.hash import password_hashing
from services.auth.token import create_access_token


auth_api = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
UserRepository = Annotated[UserRepository, Depends(get_repository(UserRepository))]


@auth_api.post("/token")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_repository: UserRepository
):
    email = form_data.username  # OAuth2 spec
    password = form_data.password
    credential_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Wrong credentials"
    )

    user = await user_repository.get_user_by_email(email)
    if not user:
        raise credential_exception

    if not password_hashing.verify_password(
        plain_password=password,
        hashed_password=user.hashed_password
    ):
        raise credential_exception

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_repo: UserRepository
):
    credential_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(
            token=token,
            key=os.environ.get("SECRET_KEY"),
            algorithms=os.environ.get("JWT_ALGORITHM")
        )
        username: str = payload.get("sub")
        if username is None:
            raise credential_exceptions
        token_data = TokenData(email=username)

    except JWTError:
        raise credential_exceptions

    user = await user_repo.get_user_by_email(token_data.email)
    if user is None:
        raise credential_exceptions

    return user


@auth_api.get("/")
async def read_users_me(current_user: Annotated[UserAuthentication, Depends(get_current_user)]):
    return current_user
