import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.lead import LeadStatus, LeadPriority


class TagResponse(BaseModel):
    id: uuid.UUID
    name: str
    color: str
    model_config = {"from_attributes": True}


class LeadCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    company: str | None = None
    phone: str = Field(min_length=1, max_length=50)
    email: str | None = None
    website: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    zip_code: str | None = None
    industry: str | None = None
    source: str | None = None
    status: LeadStatus = LeadStatus.NEW
    assigned_user_id: uuid.UUID | None = None
    priority: LeadPriority = LeadPriority.MEDIUM
    budget: float | None = None
    notes: str | None = None
    next_follow_up_at: datetime | None = None
    call_outcome: str | None = None
    # Real Estate
    property_type: str | None = None
    property_purpose: str | None = None
    preferred_location: str | None = None
    preferred_bedrooms: int | None = None
    preferred_bathrooms: int | None = None
    min_budget: float | None = None
    max_budget: float | None = None
    currency: str = "AED"
    investment_timeline: str | None = None
    nationality: str | None = None
    tag_ids: list[uuid.UUID] = []


class LeadUpdate(BaseModel):
    first_name: str | None = Field(None, min_length=1, max_length=100)
    last_name: str | None = Field(None, min_length=1, max_length=100)
    company: str | None = None
    phone: str | None = Field(None, min_length=1, max_length=50)
    email: str | None = None
    website: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    zip_code: str | None = None
    industry: str | None = None
    source: str | None = None
    status: LeadStatus | None = None
    assigned_user_id: uuid.UUID | None = None
    priority: LeadPriority | None = None
    budget: float | None = None
    notes: str | None = None
    next_follow_up_at: datetime | None = None
    call_outcome: str | None = None
    property_type: str | None = None
    property_purpose: str | None = None
    preferred_location: str | None = None
    preferred_bedrooms: int | None = None
    preferred_bathrooms: int | None = None
    min_budget: float | None = None
    max_budget: float | None = None
    currency: str | None = None
    investment_timeline: str | None = None
    nationality: str | None = None
    tag_ids: list[uuid.UUID] | None = None


class LeadResponse(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    company: str | None
    phone: str
    email: str | None
    website: str | None
    address: str | None
    city: str | None
    state: str | None
    country: str | None
    zip_code: str | None
    industry: str | None
    source: str | None
    status: LeadStatus
    assigned_user_id: uuid.UUID | None
    priority: LeadPriority
    budget: float | None
    notes: str | None
    last_contacted_at: datetime | None
    next_follow_up_at: datetime | None
    call_outcome: str | None
    property_type: str | None
    property_purpose: str | None
    preferred_location: str | None
    preferred_bedrooms: int | None
    preferred_bathrooms: int | None
    min_budget: float | None
    max_budget: float | None
    currency: str
    investment_timeline: str | None
    nationality: str | None
    tags: list[TagResponse] = []
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class LeadBulkUpdate(BaseModel):
    lead_ids: list[uuid.UUID]
    status: LeadStatus | None = None
    assigned_user_id: uuid.UUID | None = None
    priority: LeadPriority | None = None


class LeadMerge(BaseModel):
    primary_lead_id: uuid.UUID
    duplicate_lead_ids: list[uuid.UUID]
