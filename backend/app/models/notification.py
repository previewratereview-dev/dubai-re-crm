import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Text, Boolean, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class NotificationType(str, enum.Enum):
    APPOINTMENT = "appointment"
    CAMPAIGN = "campaign"
    LEAD = "lead"
    FOLLOW_UP = "follow_up"
    SYSTEM = "system"
    ERROR = "error"


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[NotificationType] = mapped_column(Enum(NotificationType), nullable=False)
    read: Mapped[bool] = mapped_column(Boolean, default=False)
    link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default="now()")

    user = relationship("User", foreign_keys=[user_id], lazy="selectin")
