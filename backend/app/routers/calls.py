import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.call import CallResponse
from app.schemas.common import PaginatedResponse
from app.services.call import CallService
from math import ceil

router = APIRouter(prefix="/api/calls", tags=["Calls"])


@router.get("", response_model=PaginatedResponse)
async def list_calls(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CallService(db)
    calls, total = await service.get_all(page, per_page)
    return PaginatedResponse(
        items=[CallResponse.model_validate(c) for c in calls],
        total=total, page=page, per_page=per_page, total_pages=ceil(total / per_page),
    )


@router.get("/{call_id}", response_model=CallResponse)
async def get_call(
    call_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CallService(db)
    call = await service.get_by_id(call_id)
    if not call:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")
    return CallResponse.model_validate(call)
