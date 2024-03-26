from typing import AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings

DB_URL = f"postgresql+asyncpg://{settings.DB.USERNAME}:{settings.DB.PASSWORD}" \
         f"@{settings.DB.HOST}:{settings.DB.PORT}/{settings.DB.NAME}"

async_engine = create_async_engine(DB_URL, poolclass=NullPool, echo=False)
async_session_marker = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_marker() as session:
        yield session


class BaseModel(DeclarativeBase):
    pass
