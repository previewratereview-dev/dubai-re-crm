import uuid
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notification import Notification


class NotificationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user(self, user_id: uuid.UUID, unread_only: bool = False, limit: int = 50) -> list[Notification]:
        stmt = select(Notification).where(Notification.user_id == user_id)
        if unread_only:
            stmt = stmt.where(Notification.read == False)
        result = await self.db.execute(stmt.order_by(Notification.created_at.desc()).limit(limit))
        return list(result.scalars().all())

    async def get_unread_count(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.count()).select_from(Notification).where(
                Notification.user_id == user_id, Notification.read == False
            )
        )
        return result.scalar() or 0

    async def create(self, **kwargs) -> Notification:
        notif = Notification(**kwargs)
        self.db.add(notif)
        await self.db.flush()
        await self.db.refresh(notif)
        return notif

    async def mark_read(self, id: uuid.UUID) -> bool:
        result = await self.db.execute(select(Notification).where(Notification.id == id))
        notif = result.scalar_one_or_none()
        if notif:
            notif.read = True
            await self.db.flush()
            return True
        return False

    async def mark_all_read(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(
            update(Notification).where(
                Notification.user_id == user_id, Notification.read == False
            ).values(read=True)
        )
        await self.db.flush()
        return result.rowcount
