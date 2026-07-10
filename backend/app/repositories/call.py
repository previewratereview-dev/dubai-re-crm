import uuid
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.call import Call
from app.repositories.base import BaseRepository


class CallRepository(BaseRepository[Call]):
    def __init__(self, db: AsyncSession):
        super().__init__(Call, db)

    async def get_by_call_id(self, call_id: str) -> Call | None:
        result = await self.db.execute(select(Call).where(Call.call_id == call_id))
        return result.scalar_one_or_none()

    async def get_by_lead(self, lead_id: uuid.UUID, limit: int = 50) -> list[Call]:
        result = await self.db.execute(
            select(Call).where(Call.lead_id == lead_id).order_by(Call.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_customer(self, customer_id: uuid.UUID, limit: int = 50) -> list[Call]:
        result = await self.db.execute(
            select(Call).where(Call.customer_id == customer_id).order_by(Call.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())

    async def count_today(self) -> int:
        from datetime import date, datetime
        today = date.today()
        start = datetime.combine(today, datetime.min.time())
        end = datetime.combine(today, datetime.max.time())
        result = await self.db.execute(
            select(func.count()).select_from(Call).where(Call.created_at.between(start, end))
        )
        return result.scalar() or 0

    async def count_answered_today(self) -> int:
        from datetime import date, datetime
        today = date.today()
        start = datetime.combine(today, datetime.min.time())
        end = datetime.combine(today, datetime.max.time())
        result = await self.db.execute(
            select(func.count()).select_from(Call).where(
                Call.created_at.between(start, end),
                Call.duration > 0,
            )
        )
        return result.scalar() or 0

    async def count_missed_today(self) -> int:
        from datetime import date, datetime
        today = date.today()
        start = datetime.combine(today, datetime.min.time())
        end = datetime.combine(today, datetime.max.time())
        result = await self.db.execute(
            select(func.count()).select_from(Call).where(
                Call.created_at.between(start, end),
                Call.duration == 0,
            )
        )
        return result.scalar() or 0

    async def get_avg_duration(self, days: int = 30) -> float:
        from datetime import datetime, timedelta
        since = datetime.utcnow() - timedelta(days=days)
        result = await self.db.execute(
            select(func.avg(Call.duration)).where(Call.created_at >= since)
        )
        return float(result.scalar() or 0)
