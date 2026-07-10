import uuid
from datetime import datetime
from pydantic import BaseModel
from app.models.call import CallDirection


class CallResponse(BaseModel):
    id: uuid.UUID
    call_id: str
    direction: CallDirection
    duration: int
    phone_number: str
    lead_id: uuid.UUID | None
    customer_id: uuid.UUID | None
    campaign_id: uuid.UUID | None
    agent_id: uuid.UUID | None
    twilio_sid: str | None
    transcript_url: str | None
    recording_url: str | None
    outcome: str | None
    appointment_created: bool
    lead_status_changed: bool
    metadata: dict | None
    created_at: datetime
    model_config = {"from_attributes": True}


class CallCreate(BaseModel):
    call_id: str
    direction: CallDirection
    duration: int = 0
    phone_number: str
    lead_id: uuid.UUID | None = None
    customer_id: uuid.UUID | None = None
    campaign_id: uuid.UUID | None = None
    agent_id: uuid.UUID | None = None
    twilio_sid: str | None = None
    transcript_url: str | None = None
    recording_url: str | None = None
    outcome: str | None = None
    metadata: dict | None = None
