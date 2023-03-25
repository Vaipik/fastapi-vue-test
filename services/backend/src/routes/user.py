from fastapi import APIRouter

from src.schemas.user import UserAuthentication

user_api = APIRouter(
    prefix="user",
    tags=["users"]
)


@user_api.post(
    path="/"
)
def create_user(user: UserAuthentication):
    return user
