import uuid
from datetime import datetime
from pydantic import BaseModel
from app.models.ticket import TicketStatus, TicketPriority


class TicketCreate(BaseModel):
    subject: str
    description: str
    customer_id: uuid.UUID
    assigned_user_id: uuid.UUID | None = None
    priority: TicketPriority = TicketPriority.MEDIUM


class TicketUpdate(BaseModel):
    subject: str | None = None
    description: str | None = None
    assigned_user_id: uuid.UUID | None = None
    status: TicketStatus | None = None
    priority: TicketPriority | None = None


class TicketResponse(BaseModel):
    id: uuid.UUID
    subject: str
    description: str
    customer_id: uuid.UUID
    assigned_user_id: uuid.UUID | None
    status: TicketStatus
    priority: TicketPriority
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
