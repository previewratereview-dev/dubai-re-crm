from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.analytics import CallAnalytics, LeadAnalytics, CampaignAnalytics
from app.services.analytics import AnalyticsService

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/calls", response_model=CallAnalytics)
async def get_call_analytics(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AnalyticsService(db)
    return await service.get_call_analytics(days)


@router.get("/leads", response_model=LeadAnalytics)
async def get_lead_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AnalyticsService(db)
    return await service.get_lead_analytics()


@router.get("/campaigns", response_model=CampaignAnalytics)
async def get_campaign_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AnalyticsService(db)
    return await service.get_campaign_analytics()
