from typing import Any

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import (
    MultipleResultsFound as MultipleResultsFoundSA,
    NoResultFound as NoResultFoundSA,
    IntegrityError as IntegrityErrorSA,
)

from src.core.types import ID
from src.database import async_session_marker, async_engine
from src.utils.repository.base import T, RepositoryABC
from src.utils.repository.exceptions import (
    IntegrityError,
    NoResultFound,
    MultipleResultsFound
)


class SQLAlchemyRepository(RepositoryABC[T, ID]):
    model = None

    async def get(self, **filters) -> T:
        query = select(self.model).filter_by(**filters)
        async with async_engine.connect() as conn:
            result = await conn.execute(query)

            try:
                return result.one()
            except MultipleResultsFoundSA:
                raise MultipleResultsFound
            except NoResultFoundSA:
                raise NoResultFound

    async def get_by_id(self, id_: ID) -> T:
        result = await self.get(id=id_)
        return result

    async def exists(self, **filters) -> bool:
        query = select(1).select_from(self.model).filter_by(**filters)

        async with async_session_marker() as session:
            result = await session.execute(query)

        return bool(result.scalars().first())

    async def filter(self, **filters: dict) -> list[T]:
        query = select(self.model).filter_by(**filters)

        async with async_session_marker() as session:
            result = await session.execute(query)

        return result.scalars().all()

    async def create(self, data: dict[str, Any]) -> T:
        stmt = insert(self.model).values(**data).returning(self.model)

        async with async_session_marker() as session:
            try:
                result = await session.execute(stmt)
            except IntegrityErrorSA as e:
                raise IntegrityError(error_info=e.orig.args[0])

            await session.commit()

        return result.scalar_one()

    async def update(self, record_id: ID, data: dict[str, Any]) -> T:
        stmt = update(self.model).filter_by(id=record_id).values(**data).returning(self.model)

        async with async_session_marker() as session:
            try:
                result = await session.execute(stmt)
            except IntegrityErrorSA as e:
                raise IntegrityError(error_info=e.orig.args[0])

            await session.commit()

        return result.scalar_one()

    # async def delete(self, record: T) -> None:
    #     pass
