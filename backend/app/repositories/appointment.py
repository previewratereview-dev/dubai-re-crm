import uuid
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.appointment import Appointment, AppointmentStatus
from app.repositories.base import BaseRepository


class AppointmentRepository(BaseRepository[Appointment]):
    def __init__(self, db: AsyncSession):
        super().__init__(Appointment, db)

    async def get_upcoming(self, user_id: uuid.UUID | None = None, limit: int = 10) -> list[Appointment]:
        stmt = select(Appointment).where(
            Appointment.start_time >= datetime.utcnow(),
            Appointment.status.in_([AppointmentStatus.SCHEDULED, AppointmentStatus.CONFIRMED]),
        )
        if user_id:
            stmt = stmt.where(Appointment.assigned_user_id == user_id)
        result = await self.db.execute(stmt.order_by(Appointment.start_time.asc()).limit(limit))
        return list(result.scalars().all())

    async def get_by_date_range(self, start: datetime, end: datetime, user_id: uuid.UUID | None = None) -> list[Appointment]:
        stmt = select(Appointment).where(
            Appointment.start_time >= start,
            Appointment.end_time <= end,
            Appointment.deleted_at.is_(None),
        )
        if user_id:
            stmt = stmt.where(Appointment.assigned_user_id == user_id)
        result = await self.db.execute(stmt.order_by(Appointment.start_time.asc()))
        return list(result.scalars().all())

    async def count_today(self) -> int:
        from datetime import date
        today = date.today()
        start = datetime.combine(today, datetime.min.time())
        end = datetime.combine(today, datetime.max.time())
        result = await self.db.execute(
            select(func.count()).select_from(Appointment).where(
                Appointment.start_time.between(start, end),
                Appointment.deleted_at.is_(None),
            )
        )
        return result.scalar() or 0

    async def check_availability(self, user_id: uuid.UUID, start: datetime, end: datetime) -> bool:
        result = await self.db.execute(
            select(func.count()).select_from(Appointment).where(
                Appointment.assigned_user_id == user_id,
                Appointment.start_time < end,
                Appointment.end_time > start,
                Appointment.status.in_([AppointmentStatus.SCHEDULED, AppointmentStatus.CONFIRMED]),
                Appointment.deleted_at.is_(None),
            )
        )
        return (result.scalar() or 0) == 0
