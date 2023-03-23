import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


def make_connection_string() -> str:
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_host = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT")
    db_name = os.environ.get("DB_NAME")
    result = (
        f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    return result


def sa_seesionmaker():
    engine = create_async_engine(make_connection_string())
    return sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
        future=True,
        autoflush=False,
    )


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with sa_seesionmaker() as session:
        yield session
        await session.close()
