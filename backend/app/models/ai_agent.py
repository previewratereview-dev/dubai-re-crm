import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Text, Enum, DateTime, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel


class AgentStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class AIAgent(BaseModel):
    __tablename__ = "ai_agents"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    agent_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    purpose: Mapped[str | None] = mapped_column(String(255), nullable=True)
    language: Mapped[str] = mapped_column(String(10), default="en")
    phone_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[AgentStatus] = mapped_column(Enum(AgentStatus), default=AgentStatus.ACTIVE)
    knowledge_sources: Mapped[dict | None] = mapped_column(JSONB, default=list)
    prompt_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    last_updated: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
