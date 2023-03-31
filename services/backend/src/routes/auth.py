from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from dependecies.database import get_repository
from repository.user import UserRepository
from services.auth.hash import password_hashing

token_api = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@token_api.post("/token")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_repository: UserRepository = Depends(get_repository(UserRepository))
):
    email = form_data.username
    password = form_data.password
    credential_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Wrong credentials"
    )

    user = await user_repository.get_user_by_email(email)
    if not user:
        raise credential_exception

    hashed_password = password_hashing.get_password_hash(password)
    if not user.hashed_password == hashed_password:
        raise credential_exception

    return {"access_token": user.email, "token_type": "bearer"}
