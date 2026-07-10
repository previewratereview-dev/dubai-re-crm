from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.integration import Integration, IntegrationType
from app.repositories.base import BaseRepository


class IntegrationRepository(BaseRepository[Integration]):
    def __init__(self, db: AsyncSession):
        super().__init__(Integration, db)

    async def get_by_type(self, type: IntegrationType) -> Integration | None:
        result = await self.db.execute(
            select(Integration).where(Integration.type == type, Integration.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()
