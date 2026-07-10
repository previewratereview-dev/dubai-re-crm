from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
from app.models.lead import Lead, LeadStatus
from app.models.call import Call
from app.models.campaign import Campaign
from app.models.appointment import Appointment
from app.schemas.analytics import CallAnalytics, LeadAnalytics, CampaignAnalytics


class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_call_analytics(self, days: int = 30) -> CallAnalytics:
        since = datetime.utcnow() - timedelta(days=days)
        total = (await self.db.execute(
            select(func.count()).select_from(Call).where(Call.created_at >= since)
        )).scalar() or 0
        answered = (await self.db.execute(
            select(func.count()).select_from(Call).where(Call.created_at >= since, Call.duration > 0)
        )).scalar() or 0
        avg_dur = (await self.db.execute(
            select(func.avg(Call.duration)).where(Call.created_at >= since)
        )).scalar() or 0

        return CallAnalytics(
            total_calls=total,
            answered=answered,
            missed=total - answered,
            avg_duration=round(float(avg_dur), 1),
        )

    async def get_lead_analytics(self) -> LeadAnalytics:
        total = (await self.db.execute(
            select(func.count()).select_from(Lead).where(Lead.deleted_at.is_(None))
        )).scalar() or 0
        converted = (await self.db.execute(
            select(func.count()).select_from(Lead).where(
                Lead.status == LeadStatus.WON, Lead.deleted_at.is_(None)
            )
        )).scalar() or 0
        rate = round((converted / total * 100), 1) if total > 0 else 0

        status_counts = (await self.db.execute(
            select(Lead.status, func.count(Lead.id))
            .where(Lead.deleted_at.is_(None))
            .group_by(Lead.status)
        )).all()

        return LeadAnalytics(
            total_leads=total,
            converted=converted,
            conversion_rate=rate,
            by_status=[{"status": r[0].value, "count": r[1]} for r in status_counts],
        )

    async def get_campaign_analytics(self) -> CampaignAnalytics:
        total = (await self.db.execute(
            select(func.count()).select_from(Campaign).where(Campaign.deleted_at.is_(None))
        )).scalar() or 0
        return CampaignAnalytics(total_campaigns=total)
