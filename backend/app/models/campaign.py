import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Text, Enum, ForeignKey, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class CampaignType(str, enum.Enum):
    SALES = "sales"
    FOLLOW_UP = "follow_up"
    REMINDER = "reminder"
    SURVEY = "survey"
    SUPPORT = "support"


class CampaignStatus(str, enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CampaignLeadStatus(str, enum.Enum):
    PENDING = "pending"
    CALLING = "calling"
    CALLED = "called"
    COMPLETED = "completed"
    FAILED = "failed"


class Campaign(BaseModel):
    __tablename__ = "campaigns"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    type: Mapped[CampaignType] = mapped_column(Enum(CampaignType), nullable=False)
    status: Mapped[CampaignStatus] = mapped_column(Enum(CampaignStatus), default=CampaignStatus.DRAFT, index=True)
    agent_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_agents.id"), nullable=True)
    scheduled_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retry_rules: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    stats: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    agent = relationship("AIAgent", foreign_keys=[agent_id], lazy="selectin")
    campaign_leads = relationship("CampaignLead", back_populates="campaign", lazy="selectin")


class CampaignLead(BaseModel):
    __tablename__ = "campaign_leads"

    campaign_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("campaigns.id"), primary_key=True)
    lead_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("leads.id"), primary_key=True)
    status: Mapped[CampaignLeadStatus] = mapped_column(Enum(CampaignLeadStatus), default=CampaignLeadStatus.PENDING)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    last_attempt_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_outcome: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Relationships
    campaign = relationship("Campaign", back_populates="campaign_leads")
    lead = relationship("Lead", lazy="selectin")
