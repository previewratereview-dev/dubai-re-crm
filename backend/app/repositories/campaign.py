import uuid
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.campaign import Campaign, CampaignLead, CampaignStatus
from app.repositories.base import BaseRepository


class CampaignRepository(BaseRepository[Campaign]):
    def __init__(self, db: AsyncSession):
        super().__init__(Campaign, db)

    async def get_running(self) -> list[Campaign]:
        result = await self.db.execute(
            select(Campaign).where(Campaign.status == CampaignStatus.RUNNING, Campaign.deleted_at.is_(None))
        )
        return list(result.scalars().all())

    async def count_by_status(self) -> list[dict]:
        result = await self.db.execute(
            select(Campaign.status, func.count(Campaign.id))
            .where(Campaign.deleted_at.is_(None))
            .group_by(Campaign.status)
        )
        return [{"status": r[0].value, "count": r[1]} for r in result.all()]


class CampaignLeadRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_leads(self, campaign_id: uuid.UUID, lead_ids: list[uuid.UUID]) -> list[CampaignLead]:
        campaign_leads = []
        for lead_id in lead_ids:
            cl = CampaignLead(campaign_id=campaign_id, lead_id=lead_id)
            self.db.add(cl)
            campaign_leads.append(cl)
        await self.db.flush()
        return campaign_leads

    async def get_next_pending(self, campaign_id: uuid.UUID) -> CampaignLead | None:
        result = await self.db.execute(
            select(CampaignLead).where(
                CampaignLead.campaign_id == campaign_id,
                CampaignLead.status == "pending",
            ).limit(1)
        )
        return result.scalar_one_or_none()

    async def update_status(self, campaign_id: uuid.UUID, lead_id: uuid.UUID, status: str, outcome: str | None = None) -> None:
        from datetime import datetime, timezone
        result = await self.db.execute(
            select(CampaignLead).where(
                CampaignLead.campaign_id == campaign_id,
                CampaignLead.lead_id == lead_id,
            )
        )
        cl = result.scalar_one_or_none()
        if cl:
            cl.status = status
            cl.attempts += 1
            cl.last_attempt_at = datetime.now(timezone.utc)
            if outcome:
                cl.last_outcome = outcome
            await self.db.flush()
