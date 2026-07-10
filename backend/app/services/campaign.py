import uuid
from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.campaign import Campaign, CampaignLead, CampaignStatus
from app.repositories.campaign import CampaignRepository, CampaignLeadRepository
from app.schemas.campaign import CampaignCreate, CampaignUpdate


class CampaignService:
    def __init__(self, db: AsyncSession):
        self.repo = CampaignRepository(db)
        self.cl_repo = CampaignLeadRepository(db)
        self.db = db

    async def get_all(self, page: int = 1, per_page: int = 20):
        return await self.repo.get_all(page, per_page)

    async def get_by_id(self, id: uuid.UUID) -> Campaign:
        campaign = await self.repo.get_by_id(id)
        if not campaign:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
        return campaign

    async def create(self, data: CampaignCreate, user_id: uuid.UUID | None = None) -> Campaign:
        campaign = await self.repo.create(
            name=data.name,
            description=data.description,
            type=data.type,
            agent_id=data.agent_id,
            scheduled_start=data.scheduled_start,
            retry_rules=data.retry_rules,
            created_by=user_id,
        )
        if data.lead_ids:
            await self.cl_repo.add_leads(campaign.id, data.lead_ids)
            await self.db.flush()
        return campaign

    async def update(self, id: uuid.UUID, data: CampaignUpdate) -> Campaign:
        campaign = await self.repo.update(id, **data.model_dump(exclude_unset=True))
        if not campaign:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
        return campaign

    async def start(self, id: uuid.UUID) -> Campaign:
        campaign = await self.repo.update(id, status=CampaignStatus.RUNNING, started_at=datetime.now(timezone.utc))
        if not campaign:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
        return campaign

    async def pause(self, id: uuid.UUID) -> Campaign:
        campaign = await self.repo.update(id, status=CampaignStatus.PAUSED)
        if not campaign:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
        return campaign

    async def resume(self, id: uuid.UUID) -> Campaign:
        campaign = await self.repo.update(id, status=CampaignStatus.RUNNING)
        if not campaign:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
        return campaign

    async def cancel(self, id: uuid.UUID) -> Campaign:
        campaign = await self.repo.update(id, status=CampaignStatus.CANCELLED)
        if not campaign:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
        return campaign

    async def get_stats(self, id: uuid.UUID) -> dict:
        campaign = await self.get_by_id(id)
        return campaign.stats or {}
