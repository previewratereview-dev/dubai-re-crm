import uuid
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.lead import Lead, LeadStatus
from app.repositories.base import BaseRepository


class LeadRepository(BaseRepository[Lead]):
    def __init__(self, db: AsyncSession):
        super().__init__(Lead, db)

    async def search(
        self, query: str | None = None, status: LeadStatus | None = None,
        assigned_user_id: uuid.UUID | None = None, source: str | None = None,
        page: int = 1, per_page: int = 20
    ) -> tuple[list[Lead], int]:
        stmt = select(Lead).where(Lead.deleted_at.is_(None))
        count_stmt = select(func.count()).select_from(Lead).where(Lead.deleted_at.is_(None))

        if query:
            search_filter = or_(
                Lead.first_name.ilike(f"%{query}%"),
                Lead.last_name.ilike(f"%{query}%"),
                Lead.email.ilike(f"%{query}%"),
                Lead.phone.ilike(f"%{query}%"),
                Lead.company.ilike(f"%{query}%"),
            )
            stmt = stmt.where(search_filter)
            count_stmt = count_stmt.where(search_filter)

        if status:
            stmt = stmt.where(Lead.status == status)
            count_stmt = count_stmt.where(Lead.status == status)
        if assigned_user_id:
            stmt = stmt.where(Lead.assigned_user_id == assigned_user_id)
            count_stmt = count_stmt.where(Lead.assigned_user_id == assigned_user_id)
        if source:
            stmt = stmt.where(Lead.source == source)
            count_stmt = count_stmt.where(Lead.source == source)

        total = (await self.db.execute(count_stmt)).scalar() or 0
        result = await self.db.execute(
            stmt.order_by(Lead.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
        )
        return list(result.scalars().all()), total

    async def get_by_phone(self, phone: str) -> Lead | None:
        result = await self.db.execute(
            select(Lead).where(Lead.phone == phone, Lead.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Lead | None:
        result = await self.db.execute(
            select(Lead).where(Lead.email == email, Lead.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def count_by_status(self) -> list[dict]:
        result = await self.db.execute(
            select(Lead.status, func.count(Lead.id))
            .where(Lead.deleted_at.is_(None))
            .group_by(Lead.status)
        )
        return [{"status": r[0].value, "count": r[1]} for r in result.all()]

    async def count_by_source(self) -> list[dict]:
        result = await self.db.execute(
            select(Lead.source, func.count(Lead.id))
            .where(Lead.deleted_at.is_(None), Lead.source.isnot(None))
            .group_by(Lead.source)
        )
        return [{"source": r[0], "count": r[1]} for r in result.all()]

    async def get_follow_ups_due(self) -> list[Lead]:
        from datetime import datetime, timezone
        result = await self.db.execute(
            select(Lead).where(
                Lead.next_follow_up_at <= datetime.now(timezone.utc),
                Lead.next_follow_up_at.isnot(None),
                Lead.deleted_at.is_(None),
            )
        )
        return list(result.scalars().all())

    async def get_pipeline_value(self) -> float:
        result = await self.db.execute(
            select(func.sum(Lead.budget)).where(
                Lead.status.in_([
                    LeadStatus.INTERESTED, LeadStatus.APPOINTMENT_SCHEDULED,
                    LeadStatus.PROPOSAL_SENT, LeadStatus.NEGOTIATION
                ]),
                Lead.budget.isnot(None),
                Lead.deleted_at.is_(None),
            )
        )
        return float(result.scalar() or 0)
