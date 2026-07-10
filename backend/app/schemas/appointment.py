import uuid
from datetime import datetime
from pydantic import BaseModel
from app.models.appointment import AppointmentStatus


class AppointmentCreate(BaseModel):
    title: str
    description: str | None = None
    lead_id: uuid.UUID | None = None
    customer_id: uuid.UUID | None = None
    assigned_user_id: uuid.UUID
    start_time: datetime
    end_time: datetime
    timezone: str = "UTC"
    location: str | None = None
    meeting_link: str | None = None


class AppointmentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    timezone: str | None = None
    status: AppointmentStatus | None = None
    location: str | None = None
    meeting_link: str | None = None


class AppointmentResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None
    lead_id: uuid.UUID | None
    customer_id: uuid.UUID | None
    assigned_user_id: uuid.UUID
    start_time: datetime
    end_time: datetime
    timezone: str
    status: AppointmentStatus
    google_event_id: str | None
    location: str | None
    meeting_link: str | None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class AvailabilityRequest(BaseModel):
    user_id: uuid.UUID
    date: str  # YYYY-MM-DD
    duration_minutes: int = 30


class AvailabilityResponse(BaseModel):
    available_slots: list[str]  # ISO time strings
