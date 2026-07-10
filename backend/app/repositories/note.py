import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.note import Note


class NoteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_lead(self, lead_id: uuid.UUID) -> list[Note]:
        result = await self.db.execute(
            select(Note).where(Note.lead_id == lead_id).order_by(Note.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_customer(self, customer_id: uuid.UUID) -> list[Note]:
        result = await self.db.execute(
            select(Note).where(Note.customer_id == customer_id).order_by(Note.created_at.desc())
        )
        return list(result.scalars().all())

    async def create(self, **kwargs) -> Note:
        note = Note(**kwargs)
        self.db.add(note)
        await self.db.flush()
        await self.db.refresh(note)
        return note

    async def update(self, id: uuid.UUID, content: str) -> Note | None:
        result = await self.db.execute(select(Note).where(Note.id == id))
        note = result.scalar_one_or_none()
        if note:
            note.content = content
            await self.db.flush()
            await self.db.refresh(note)
        return note

    async def delete(self, id: uuid.UUID) -> bool:
        result = await self.db.execute(select(Note).where(Note.id == id))
        note = result.scalar_one_or_none()
        if note:
            await self.db.delete(note)
            await self.db.flush()
            return True
        return False
