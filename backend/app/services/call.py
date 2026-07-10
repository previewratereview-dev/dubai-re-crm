import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.call import Call
from app.repositories.call import CallRepository
from app.schemas.call import CallCreate


class CallService:
    def __init__(self, db: AsyncSession):
        self.repo = CallRepository(db)
        self.db = db

    async def get_all(self, page: int = 1, per_page: int = 20):
        return await self.repo.get_all(page, per_page)

    async def get_by_id(self, id: uuid.UUID) -> Call | None:
        return await self.repo.get_by_id(id)

    async def create(self, data: CallCreate) -> Call:
        return await self.repo.create(**data.model_dump())

    async def get_by_lead(self, lead_id: uuid.UUID) -> list[Call]:
        return await self.repo.get_by_lead(lead_id)

    async def get_by_customer(self, customer_id: uuid.UUID) -> list[Call]:
        return await self.repo.get_by_customer(customer_id)

    async def count_today(self) -> int:
        return await self.repo.count_today()

    async def count_answered_today(self) -> int:
        return await self.repo.count_answered_today()

    async def count_missed_today(self) -> int:
        return await self.repo.count_missed_today()

    async def get_avg_duration(self, days: int = 30) -> float:
        return await self.repo.get_avg_duration(days)
