import uuid
from datetime import datetime
from pydantic import BaseModel
from app.models.campaign import CampaignType, CampaignStatus


class CampaignCreate(BaseModel):
    name: str
    description: str | None = None
    type: CampaignType
    agent_id: uuid.UUID | None = None
    scheduled_start: datetime | None = None
    retry_rules: dict = {"max_attempts": 3, "business_hours_only": True, "retry_interval_hours": 24}
    lead_ids: list[uuid.UUID] = []


class CampaignUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    type: CampaignType | None = None
    agent_id: uuid.UUID | None = None
    scheduled_start: datetime | None = None
    retry_rules: dict | None = None


class CampaignResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    type: CampaignType
    status: CampaignStatus
    agent_id: uuid.UUID | None
    scheduled_start: datetime | None
    retry_rules: dict | None
    stats: dict | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class CampaignLeadResponse(BaseModel):
    id: uuid.UUID
    lead_id: uuid.UUID
    campaign_id: uuid.UUID
    status: str
    attempts: int
    last_attempt_at: datetime | None
    last_outcome: str | None
    model_config = {"from_attributes": True}
