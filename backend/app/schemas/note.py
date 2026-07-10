import uuid
from datetime import datetime
from pydantic import BaseModel


class NoteCreate(BaseModel):
    content: str
    lead_id: uuid.UUID | None = None
    customer_id: uuid.UUID | None = None


class NoteUpdate(BaseModel):
    content: str


class NoteResponse(BaseModel):
    id: uuid.UUID
    content: str
    lead_id: uuid.UUID | None
    customer_id: uuid.UUID | None
    created_by: uuid.UUID | None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
