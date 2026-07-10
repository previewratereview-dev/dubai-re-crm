from sqlalchemy.ext.asyncio import AsyncSession
from app.services.call import CallService
from app.services.appointment import AppointmentService
from app.services.lead import LeadService
from app.services.campaign import CampaignService
from app.schemas.dashboard import DashboardStats


class DashboardService:
    def __init__(self, db: AsyncSession):
        self.call_service = CallService(db)
        self.appt_service = AppointmentService(db)
        self.lead_service = LeadService(db)
        self.campaign_service = CampaignService(db)
        self.db = db

    async def get_stats(self) -> DashboardStats:
        today_calls = await self.call_service.count_today()
        today_appts = await self.appt_service.count_today()
        leads, total_leads = await self.lead_service.search(per_page=1)
        follow_ups = await self.lead_service.get_follow_ups_due()
        pipeline_value = await self.lead_service.get_pipeline_value()
        answered = await self.call_service.count_answered_today()
        missed = await self.call_service.count_missed_today()
        lead_sources = await self.lead_service.count_by_source()
        upcoming = await self.appt_service.get_upcoming(limit=5)
        campaign_stats = await self.campaign_service.repo.count_by_status()

        conversion_rate = 0
        if total_leads > 0:
            from app.models.lead import LeadStatus
            from sqlalchemy import select, func
            won = await self.db.execute(
                select(func.count()).select_from(
                    __import__("app.models.lead", fromlist=["Lead"]).Lead
                ).where(
                    __import__("app.models.lead", fromlist=["Lead"]).Lead.status == LeadStatus.WON
                )
            )
            won_count = won.scalar() or 0
            conversion_rate = round((won_count / total_leads) * 100, 1)

        return DashboardStats(
            today_calls=today_calls,
            today_appointments=today_appts,
            open_leads=total_leads,
            follow_ups_due=len(follow_ups),
            pipeline_value=pipeline_value,
            calls_answered=answered,
            calls_missed=missed,
            appointments_booked=today_appts,
            conversion_rate=conversion_rate,
            lead_sources=lead_sources,
            recent_activity=[],
            campaign_status=campaign_stats,
            upcoming_meetings=[
                {"id": str(m.id), "title": m.title, "time": m.start_time.isoformat()}
                for m in upcoming
            ],
        )
