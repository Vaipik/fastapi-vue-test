from typing import Optional

import sqlalchemy as sa

from models.user import User
from repository.base import BaseRepository
from schemas.user import UserAuthentication, UserProfile
from services.auth.hash import password_hashing


class UserRepository(BaseRepository):

    async def get_user_by_email(self, email: str) -> Optional[User]:
        user = await self._session.get(User, email)
        return user

    async def create_user(self, credentials: UserAuthentication) -> User:
        user = User(
            email=credentials.email,
            hashed_password=password_hashing.get_password_hash(credentials.password)
        )
        self._session.add(user)
        await self._session.commit()
        return user

    async def update_user_profile(self, user_email: str, data: UserProfile) -> User:
        profile_data = data.dict()
        user = await self.get_user_by_email(user_email)
        if user is None:
            pass # TODO: Raise Error

        update_stmt = sa.update(table=User) \
            .where(User.email == user_email)

        if profile_data["first_name"]:
            update_stmt = update_stmt.values(first_name=profile_data["first_name"])

        if profile_data["last_name"]:
            update_stmt = update_stmt.values(last_name=profile_data["last_name"])

        if profile_data["sex"]:
            update_stmt = update_stmt.values(sex=profile_data["last_name"])

        await self._session.execute(statement=update_stmt)
        await self._session.commit()
        await self._session.refresh(instance=user)

        return user
