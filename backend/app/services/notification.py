import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.notification import NotificationRepository
from app.models.notification import NotificationType


class NotificationService:
    def __init__(self, db: AsyncSession):
        self.repo = NotificationRepository(db)
        self.db = db

    async def get_by_user(self, user_id: uuid.UUID, unread_only: bool = False):
        return await self.repo.get_by_user(user_id, unread_only)

    async def get_unread_count(self, user_id: uuid.UUID) -> int:
        return await self.repo.get_unread_count(user_id)

    async def create(self, user_id: uuid.UUID, title: str, message: str, type: NotificationType, link: str | None = None):
        return await self.repo.create(user_id=user_id, title=title, message=message, type=type, link=link)

    async def mark_read(self, id: uuid.UUID) -> bool:
        return await self.repo.mark_read(id)

    async def mark_all_read(self, user_id: uuid.UUID) -> int:
        return await self.repo.mark_all_read(user_id)
