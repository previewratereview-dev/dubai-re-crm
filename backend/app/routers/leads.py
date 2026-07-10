import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.user import User, UserRole
from app.models.lead import LeadStatus
from app.schemas.lead import LeadCreate, LeadUpdate, LeadResponse, LeadBulkUpdate, LeadMerge
from app.schemas.common import PaginatedResponse, MessageResponse
from app.services.lead import LeadService
from math import ceil

router = APIRouter(prefix="/api/leads", tags=["Leads"])


@router.get("", response_model=PaginatedResponse)
async def list_leads(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    q: str | None = None,
    status: LeadStatus | None = None,
    assigned_user_id: uuid.UUID | None = None,
    source: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = LeadService(db)
    leads, total = await service.search(q, status, assigned_user_id, source, page, per_page)
    return PaginatedResponse(
        items=[LeadResponse.model_validate(l) for l in leads],
        total=total, page=page, per_page=per_page, total_pages=ceil(total / per_page),
    )


@router.post("", response_model=LeadResponse, status_code=201)
async def create_lead(
    data: LeadCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = LeadService(db)
    lead = await service.create(data, current_user.id)
    return LeadResponse.model_validate(lead)


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = LeadService(db)
    lead = await service.get_by_id(lead_id)
    return LeadResponse.model_validate(lead)


@router.put("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: uuid.UUID,
    data: LeadUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = LeadService(db)
    lead = await service.update(lead_id, data)
    return LeadResponse.model_validate(lead)


@router.delete("/{lead_id}", response_model=MessageResponse)
async def delete_lead(
    lead_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.SALES)),
):
    service = LeadService(db)
    await service.delete(lead_id)
    return MessageResponse(message="Lead deleted")


@router.post("/bulk-update", response_model=MessageResponse)
async def bulk_update_leads(
    data: LeadBulkUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = LeadService(db)
    count = await service.bulk_update(data)
    return MessageResponse(message=f"Updated {count} leads")


@router.post("/import")
async def import_leads(
    csv_content: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = LeadService(db)
    return await service.import_csv(csv_content, current_user.id)


@router.get("/export/csv")
async def export_leads(
    lead_ids: list[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = LeadService(db)
    csv = await service.export_csv(lead_ids)
    return {"csv": csv}


@router.post("/merge", response_model=LeadResponse)
async def merge_leads(
    data: LeadMerge,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN)),
):
    service = LeadService(db)
    lead = await service.merge(data.primary_lead_id, data.duplicate_lead_ids)
    return LeadResponse.model_validate(lead)


@router.post("/{lead_id}/assign", response_model=LeadResponse)
async def assign_lead(
    lead_id: uuid.UUID,
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = LeadService(db)
    lead = await service.assign_user(lead_id, user_id)
    return LeadResponse.model_validate(lead)
