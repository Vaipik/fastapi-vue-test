from fastapi import APIRouter, Depends

from dependecies.database import get_repository
from repository.user import UserRepository
from schemas.user import UserAuthentication, UserProfile, UserInDB

user_api = APIRouter(
    prefix="/user",
    tags=["users"]
)


@user_api.post(
    path="/",
    response_model=UserInDB
)
async def create_user(
        credentials: UserAuthentication,
        user_repo: UserRepository = Depends(get_repository(UserRepository))
):
    user = await user_repo.create_user(credentials)
    return user


@user_api.post(
    path="/profile"
)
async def update_profile(
        profile: UserProfile,
        user_repo: UserRepository = Depends(get_repository(UserRepository))
):
    user_email = "email@com.ua"
    updated_profile = await user_repo.update_user_profile(user_email, profile)
    return updated_profile
