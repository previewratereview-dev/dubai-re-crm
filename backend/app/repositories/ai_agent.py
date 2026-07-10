from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ai_agent import AIAgent
from app.repositories.base import BaseRepository


class AIAgentRepository(BaseRepository[AIAgent]):
    def __init__(self, db: AsyncSession):
        super().__init__(AIAgent, db)

    async def get_by_agent_id(self, agent_id: str) -> AIAgent | None:
        result = await self.db.execute(
            select(AIAgent).where(AIAgent.agent_id == agent_id, AIAgent.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()
