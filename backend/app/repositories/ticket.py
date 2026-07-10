import uuid
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ticket import Ticket
from app.repositories.base import BaseRepository


class TicketRepository(BaseRepository[Ticket]):
    def __init__(self, db: AsyncSession):
        super().__init__(Ticket, db)

    async def get_by_customer(self, customer_id: uuid.UUID) -> list[Ticket]:
        result = await self.db.execute(
            select(Ticket).where(Ticket.customer_id == customer_id, Ticket.deleted_at.is_(None))
            .order_by(Ticket.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_open_count(self) -> int:
        from app.models.ticket import TicketStatus
        result = await self.db.execute(
            select(func.count()).select_from(Ticket).where(
                Ticket.status.in_([TicketStatus.OPEN, TicketStatus.IN_PROGRESS]),
                Ticket.deleted_at.is_(None),
            )
        )
        return result.scalar() or 0
