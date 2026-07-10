import uuid
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.appointment import Appointment, AppointmentStatus
from app.repositories.appointment import AppointmentRepository
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate


class AppointmentService:
    def __init__(self, db: AsyncSession):
        self.repo = AppointmentRepository(db)
        self.db = db

    async def get_all(self, page: int = 1, per_page: int = 20):
        return await self.repo.get_all(page, per_page)

    async def get_by_id(self, id: uuid.UUID) -> Appointment:
        appt = await self.repo.get_by_id(id)
        if not appt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
        return appt

    async def get_upcoming(self, user_id: uuid.UUID | None = None, limit: int = 10):
        return await self.repo.get_upcoming(user_id, limit)

    async def book(self, data: AppointmentCreate, user_id: uuid.UUID | None = None) -> Appointment:
        available = await self.repo.check_availability(
            data.assigned_user_id, data.start_time, data.end_time
        )
        if not available:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Time slot not available")
        return await self.repo.create(**data.model_dump(), created_by=user_id)

    async def reschedule(self, id: uuid.UUID, data: AppointmentUpdate) -> Appointment:
        appt = await self.get_by_id(id)
        if data.start_time and data.end_time:
            available = await self.repo.check_availability(
                appt.assigned_user_id, data.start_time, data.end_time
            )
            if not available:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New time slot not available")
        updated = await self.repo.update(id, **data.model_dump(exclude_unset=True))
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
        return updated

    async def cancel(self, id: uuid.UUID) -> Appointment:
        updated = await self.repo.update(id, status=AppointmentStatus.CANCELLED)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
        return updated

    async def check_availability(self, user_id: uuid.UUID, date_str: str, duration_minutes: int = 30) -> list[str]:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        start_of_day = date_obj.replace(hour=8, minute=0, second=0)
        end_of_day = date_obj.replace(hour=18, minute=0, second=0)
        existing = await self.repo.get_by_date_range(start_of_day, end_of_day, user_id)
        booked_slots = set()
        for appt in existing:
            slot = appt.start_time.strftime("%H:%M")
            booked_slots.add(slot)
        available = []
        current = start_of_day
        while current + timedelta(minutes=duration_minutes) <= end_of_day:
            slot = current.strftime("%H:%M")
            if slot not in booked_slots:
                available.append(slot)
            current += timedelta(minutes=30)
        return available

    async def count_today(self) -> int:
        return await self.repo.count_today()
