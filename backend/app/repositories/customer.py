import uuid
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.customer import Customer
from app.repositories.base import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    def __init__(self, db: AsyncSession):
        super().__init__(Customer, db)

    async def search(
        self, query: str | None = None, page: int = 1, per_page: int = 20
    ) -> tuple[list[Customer], int]:
        stmt = select(Customer).where(Customer.deleted_at.is_(None))
        count_stmt = select(func.count()).select_from(Customer).where(Customer.deleted_at.is_(None))

        if query:
            search_filter = or_(
                Customer.first_name.ilike(f"%{query}%"),
                Customer.last_name.ilike(f"%{query}%"),
                Customer.email.ilike(f"%{query}%"),
                Customer.phone.ilike(f"%{query}%"),
                Customer.company.ilike(f"%{query}%"),
            )
            stmt = stmt.where(search_filter)
            count_stmt = count_stmt.where(search_filter)

        total = (await self.db.execute(count_stmt)).scalar() or 0
        result = await self.db.execute(
            stmt.order_by(Customer.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
        )
        return list(result.scalars().all()), total

    async def get_by_email(self, email: str) -> Customer | None:
        result = await self.db.execute(
            select(Customer).where(Customer.email == email, Customer.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()
