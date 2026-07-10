import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ai_agent import AIAgent
from app.repositories.ai_agent import AIAgentRepository
from app.schemas.ai_agent import AIAgentCreate, AIAgentUpdate


class AIAgentService:
    def __init__(self, db: AsyncSession):
        self.repo = AIAgentRepository(db)
        self.db = db

    async def get_all(self, page: int = 1, per_page: int = 20):
        return await self.repo.get_all(page, per_page)

    async def get_by_id(self, id: uuid.UUID) -> AIAgent:
        agent = await self.repo.get_by_id(id)
        if not agent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AI Agent not found")
        return agent

    async def create(self, data: AIAgentCreate) -> AIAgent:
        return await self.repo.create(**data.model_dump())

    async def update(self, id: uuid.UUID, data: AIAgentUpdate) -> AIAgent:
        agent = await self.repo.update(id, **data.model_dump(exclude_unset=True))
        if not agent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AI Agent not found")
        return agent

    async def delete(self, id: uuid.UUID) -> bool:
        return await self.repo.soft_delete(id)
