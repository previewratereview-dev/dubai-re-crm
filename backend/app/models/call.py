import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Boolean, Enum, ForeignKey, Integer, DateTime, JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class CallDirection(str, enum.Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class Call(Base):
    __tablename__ = "calls"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    call_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    direction: Mapped[CallDirection] = mapped_column(Enum(CallDirection), nullable=False)
    duration: Mapped[int] = mapped_column(Integer, default=0)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=False)
    lead_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("leads.id"), nullable=True, index=True)
    customer_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True, index=True)
    campaign_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("campaigns.id"), nullable=True, index=True)
    agent_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_agents.id"), nullable=True)
    twilio_sid: Mapped[str | None] = mapped_column(String(255), nullable=True)
    transcript_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    recording_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    outcome: Mapped[str | None] = mapped_column(String(100), nullable=True)
    appointment_created: Mapped[bool] = mapped_column(Boolean, default=False)
    lead_status_changed: Mapped[bool] = mapped_column(Boolean, default=False)
    metadata: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default="now()")

    # Relationships
    lead = relationship("Lead", foreign_keys=[lead_id], lazy="selectin")
    customer = relationship("Customer", foreign_keys=[customer_id], lazy="selectin")
    campaign = relationship("Campaign", foreign_keys=[campaign_id], lazy="selectin")
    agent = relationship("AIAgent", foreign_keys=[agent_id], lazy="selectin")
