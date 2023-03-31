from typing import Type, Callable, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.connection import sa_sessionmaker
from repository.base import BaseRepository


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with sa_sessionmaker() as session:
        yield session
        await session.close()


def get_repository(repo_type: Type[BaseRepository]) -> Callable:
    def get_repo(session: AsyncSession = Depends(get_async_session)) -> Type[BaseRepository]:
        return repo_type(session)  # type: ignore

    return get_repo
