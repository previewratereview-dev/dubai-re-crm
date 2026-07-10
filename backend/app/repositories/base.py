import uuid
from typing import TypeVar, Generic, Type
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_by_id(self, id: uuid.UUID) -> ModelType | None:
        result = await self.db.execute(
            select(self.model).where(self.model.id == id, self.model.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def get_all(self, page: int = 1, per_page: int = 20) -> tuple[list[ModelType], int]:
        query = select(self.model).where(self.model.deleted_at.is_(None))
        count_query = select(func.count()).select_from(self.model).where(self.model.deleted_at.is_(None))

        total = (await self.db.execute(count_query)).scalar() or 0
        result = await self.db.execute(query.offset((page - 1) * per_page).limit(per_page))
        return list(result.scalars().all()), total

    async def create(self, **kwargs) -> ModelType:
        obj = self.model(**kwargs)
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def update(self, id: uuid.UUID, **kwargs) -> ModelType | None:
        obj = await self.get_by_id(id)
        if not obj:
            return None
        for key, value in kwargs.items():
            if value is not None and hasattr(obj, key):
                setattr(obj, key, value)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def soft_delete(self, id: uuid.UUID) -> bool:
        from datetime import datetime, timezone
        obj = await self.get_by_id(id)
        if not obj:
            return False
        obj.deleted_at = datetime.now(timezone.utc)
        await self.db.flush()
        return True

    async def count(self) -> int:
        result = await self.db.execute(
            select(func.count()).select_from(self.model).where(self.model.deleted_at.is_(None))
        )
        return result.scalar() or 0
