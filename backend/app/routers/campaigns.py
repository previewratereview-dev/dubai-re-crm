import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.user import User, UserRole
from app.schemas.campaign import CampaignCreate, CampaignUpdate, CampaignResponse
from app.schemas.common import PaginatedResponse, MessageResponse
from app.services.campaign import CampaignService
from math import ceil

router = APIRouter(prefix="/api/campaigns", tags=["Campaigns"])


@router.get("", response_model=PaginatedResponse)
async def list_campaigns(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CampaignService(db)
    campaigns, total = await service.get_all(page, per_page)
    return PaginatedResponse(
        items=[CampaignResponse.model_validate(c) for c in campaigns],
        total=total, page=page, per_page=per_page, total_pages=ceil(total / per_page),
    )


@router.post("", response_model=CampaignResponse, status_code=201)
async def create_campaign(
    data: CampaignCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CampaignService(db)
    campaign = await service.create(data, current_user.id)
    return CampaignResponse.model_validate(campaign)


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CampaignService(db)
    campaign = await service.get_by_id(campaign_id)
    return CampaignResponse.model_validate(campaign)


@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: uuid.UUID,
    data: CampaignUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CampaignService(db)
    campaign = await service.update(campaign_id, data)
    return CampaignResponse.model_validate(campaign)


@router.post("/{campaign_id}/start", response_model=CampaignResponse)
async def start_campaign(
    campaign_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CampaignService(db)
    campaign = await service.start(campaign_id)
    return CampaignResponse.model_validate(campaign)


@router.post("/{campaign_id}/pause", response_model=CampaignResponse)
async def pause_campaign(
    campaign_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CampaignService(db)
    campaign = await service.pause(campaign_id)
    return CampaignResponse.model_validate(campaign)


@router.post("/{campaign_id}/resume", response_model=CampaignResponse)
async def resume_campaign(
    campaign_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CampaignService(db)
    campaign = await service.resume(campaign_id)
    return CampaignResponse.model_validate(campaign)


@router.post("/{campaign_id}/cancel", response_model=CampaignResponse)
async def cancel_campaign(
    campaign_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CampaignService(db)
    campaign = await service.cancel(campaign_id)
    return CampaignResponse.model_validate(campaign)


@router.get("/{campaign_id}/stats")
async def get_campaign_stats(
    campaign_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CampaignService(db)
    return await service.get_stats(campaign_id)
