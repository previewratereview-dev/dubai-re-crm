import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.note import NoteRepository
from app.schemas.note import NoteCreate, NoteUpdate


class NoteService:
    def __init__(self, db: AsyncSession):
        self.repo = NoteRepository(db)
        self.db = db

    async def get_by_lead(self, lead_id: uuid.UUID):
        return await self.repo.get_by_lead(lead_id)

    async def get_by_customer(self, customer_id: uuid.UUID):
        return await self.repo.get_by_customer(customer_id)

    async def create(self, data: NoteCreate, user_id: uuid.UUID | None = None):
        return await self.repo.create(**data.model_dump(), created_by=user_id)

    async def update(self, id: uuid.UUID, data: NoteUpdate):
        return await self.repo.update(id, data.content)

    async def delete(self, id: uuid.UUID):
        return await self.repo.delete(id)
