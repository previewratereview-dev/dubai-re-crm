import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ticket import Ticket
from app.repositories.ticket import TicketRepository
from app.schemas.ticket import TicketCreate, TicketUpdate


class TicketService:
    def __init__(self, db: AsyncSession):
        self.repo = TicketRepository(db)
        self.db = db

    async def get_all(self, page: int = 1, per_page: int = 20):
        return await self.repo.get_all(page, per_page)

    async def get_by_id(self, id: uuid.UUID) -> Ticket:
        ticket = await self.repo.get_by_id(id)
        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
        return ticket

    async def create(self, data: TicketCreate, user_id: uuid.UUID | None = None) -> Ticket:
        return await self.repo.create(**data.model_dump(), created_by=user_id)

    async def update(self, id: uuid.UUID, data: TicketUpdate) -> Ticket:
        ticket = await self.repo.update(id, **data.model_dump(exclude_unset=True))
        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
        return ticket

    async def delete(self, id: uuid.UUID) -> bool:
        return await self.repo.soft_delete(id)
