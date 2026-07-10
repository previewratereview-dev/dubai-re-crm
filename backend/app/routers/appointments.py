import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.appointment import (
    AppointmentCreate, AppointmentUpdate, AppointmentResponse,
    AvailabilityRequest, AvailabilityResponse,
)
from app.schemas.common import PaginatedResponse, MessageResponse
from app.services.appointment import AppointmentService
from math import ceil

router = APIRouter(prefix="/api/appointments", tags=["Appointments"])


@router.get("", response_model=PaginatedResponse)
async def list_appointments(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AppointmentService(db)
    appts, total = await service.get_all(page, per_page)
    return PaginatedResponse(
        items=[AppointmentResponse.model_validate(a) for a in appts],
        total=total, page=page, per_page=per_page, total_pages=ceil(total / per_page),
    )


@router.post("", response_model=AppointmentResponse, status_code=201)
async def book_appointment(
    data: AppointmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AppointmentService(db)
    appt = await service.book(data, current_user.id)
    return AppointmentResponse.model_validate(appt)


@router.get("/upcoming")
async def get_upcoming(
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AppointmentService(db)
    appts = await service.get_upcoming(limit=limit)
    return [AppointmentResponse.model_validate(a) for a in appts]


@router.get("/availability", response_model=AvailabilityResponse)
async def check_availability(
    user_id: uuid.UUID = Query(...),
    date: str = Query(...),
    duration_minutes: int = Query(30, ge=15, le=480),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AppointmentService(db)
    slots = await service.check_availability(user_id, date, duration_minutes)
    return AvailabilityResponse(available_slots=slots)


@router.get("/{appt_id}", response_model=AppointmentResponse)
async def get_appointment(
    appt_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AppointmentService(db)
    appt = await service.get_by_id(appt_id)
    return AppointmentResponse.model_validate(appt)


@router.put("/{appt_id}", response_model=AppointmentResponse)
async def reschedule_appointment(
    appt_id: uuid.UUID,
    data: AppointmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AppointmentService(db)
    appt = await service.reschedule(appt_id, data)
    return AppointmentResponse.model_validate(appt)


@router.delete("/{appt_id}", response_model=MessageResponse)
async def cancel_appointment(
    appt_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AppointmentService(db)
    await service.cancel(appt_id)
    return MessageResponse(message="Appointment cancelled")
