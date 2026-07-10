import uuid
from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    color: Mapped[str] = mapped_column(String(7), default="#3B82F6")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default="now()")

    leads = relationship("Lead", secondary="lead_tags", back_populates="tags", lazy="selectin")
    customers = relationship("Customer", secondary="customer_tags", back_populates="tags", lazy="selectin")
