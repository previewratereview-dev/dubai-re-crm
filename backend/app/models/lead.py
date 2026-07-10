import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Text, Numeric, Integer, Enum, ForeignKey, Table, Column, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class LeadStatus(str, enum.Enum):
    NEW = "new"
    ATTEMPTING_CONTACT = "attempting_contact"
    CONNECTED = "connected"
    INTERESTED = "interested"
    APPOINTMENT_SCHEDULED = "appointment_scheduled"
    PROPOSAL_SENT = "proposal_sent"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"
    BUSY = "busy"
    VOICEMAIL = "voicemail"
    WRONG_NUMBER = "wrong_number"
    NO_ANSWER = "no_answer"
    FOLLOW_UP = "follow_up"
    DO_NOT_CONTACT = "do_not_contact"


class LeadPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class PropertyType(str, enum.Enum):
    APARTMENT = "apartment"
    VILLA = "villa"
    TOWNHOUSE = "townhouse"
    PENTHOUSE = "penthouse"
    OFFICE = "office"
    LAND = "land"
    WAREHOUSE = "warehouse"
    RETAIL = "retail"
    OTHER = "other"


class PropertyPurpose(str, enum.Enum):
    BUY = "buy"
    RENT = "rent"
    INVEST = "invest"


class InvestmentTimeline(str, enum.Enum):
    IMMEDIATE = "immediate"
    THREE_MONTHS = "3_months"
    SIX_MONTHS = "6_months"
    ONE_YEAR = "1_year"
    FLEXIBLE = "flexible"


lead_tags = Table(
    "lead_tags",
    BaseModel.metadata,
    Column("lead_id", UUID(as_uuid=True), ForeignKey("leads.id"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True),
)


class Lead(BaseModel):
    __tablename__ = "leads"

    # Basic info
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Address
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    zip_code: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # Business
    industry: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    status: Mapped[LeadStatus] = mapped_column(Enum(LeadStatus), default=LeadStatus.NEW, index=True)
    assigned_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    priority: Mapped[LeadPriority] = mapped_column(Enum(LeadPriority), default=LeadPriority.MEDIUM)
    budget: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Activity
    last_contacted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    next_follow_up_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    appointment_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("appointments.id"), nullable=True)
    call_outcome: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Real Estate
    property_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    property_purpose: Mapped[str | None] = mapped_column(String(50), nullable=True)
    preferred_location: Mapped[str | None] = mapped_column(Text, nullable=True)
    preferred_bedrooms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    preferred_bathrooms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    min_budget: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    max_budget: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="AED")
    investment_timeline: Mapped[str | None] = mapped_column(String(50), nullable=True)
    nationality: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Relationships
    tags = relationship("Tag", secondary=lead_tags, back_populates="leads", lazy="selectin")
    assigned_user = relationship("User", foreign_keys=[assigned_user_id], lazy="selectin")
    appointment = relationship("Appointment", foreign_keys=[appointment_id], lazy="selectin")


class LeadTag(BaseModel):
    __tablename__ = "lead_tag_details"

    lead_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("leads.id"), primary_key=True)
    tag_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True)
