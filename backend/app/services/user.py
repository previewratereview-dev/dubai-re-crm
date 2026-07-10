import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
        self.db = db

    async def get_all(self, page: int = 1, per_page: int = 20) -> tuple[list[User], int]:
        return await self.repo.get_all(page, per_page)

    async def get_by_id(self, id: uuid.UUID) -> User:
        user = await self.repo.get_by_id(id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def create(self, data: UserCreate, created_by: uuid.UUID | None = None) -> User:
        from app.services.auth import register_user
        return await register_user(self.db, data, created_by)

    async def update(self, id: uuid.UUID, data: UserUpdate) -> User:
        user = await self.repo.update(id, **data.model_dump(exclude_unset=True))
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def deactivate(self, id: uuid.UUID) -> bool:
        return await self.repo.soft_delete(id)
