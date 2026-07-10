import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    lead_id: uuid.UUID | None = None
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    company: str | None = None
    phone: str = Field(min_length=1, max_length=50)
    email: str = Field(min_length=1)
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    zip_code: str | None = None
    industry: str | None = None
    notes: str | None = None
    tag_ids: list[uuid.UUID] = []


class CustomerUpdate(BaseModel):
    first_name: str | None = Field(None, min_length=1, max_length=100)
    last_name: str | None = Field(None, min_length=1, max_length=100)
    company: str | None = None
    phone: str | None = Field(None, min_length=1, max_length=50)
    email: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    zip_code: str | None = None
    industry: str | None = None
    notes: str | None = None
    tag_ids: list[uuid.UUID] | None = None


class CustomerResponse(BaseModel):
    id: uuid.UUID
    lead_id: uuid.UUID | None
    first_name: str
    last_name: str
    company: str | None
    phone: str
    email: str
    address: str | None
    city: str | None
    state: str | None
    country: str | None
    zip_code: str | None
    industry: str | None
    notes: str | None
    purchase_history: dict | None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
