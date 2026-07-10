import uuid
from datetime import datetime
from pydantic import BaseModel
from app.models.notification import NotificationType


class NotificationResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    message: str
    type: NotificationType
    read: bool
    link: str | None
    created_at: datetime
    model_config = {"from_attributes": True}
