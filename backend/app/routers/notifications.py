import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.notification import NotificationResponse
from app.schemas.common import MessageResponse
from app.services.notification import NotificationService

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@router.get("", response_model=list[NotificationResponse])
async def list_notifications(
    unread_only: bool = Query(False),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NotificationService(db)
    notifs = await service.get_by_user(current_user.id, unread_only)
    return [NotificationResponse.model_validate(n) for n in notifs]


@router.get("/unread-count")
async def get_unread_count(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NotificationService(db)
    count = await service.get_unread_count(current_user.id)
    return {"count": count}


@router.put("/{notification_id}/read", response_model=MessageResponse)
async def mark_read(
    notification_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NotificationService(db)
    await service.mark_read(notification_id)
    return MessageResponse(message="Marked as read")


@router.put("/read-all", response_model=MessageResponse)
async def mark_all_read(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NotificationService(db)
    count = await service.mark_all_read(current_user.id)
    return MessageResponse(message=f"Marked {count} notifications as read")
