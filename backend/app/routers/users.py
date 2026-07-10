import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import require_role
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.common import PaginatedResponse, MessageResponse
from app.services.user import UserService
from math import ceil

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("", response_model=PaginatedResponse)
async def list_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN)),
):
    service = UserService(db)
    users, total = await service.get_all(page, per_page)
    return PaginatedResponse(
        items=[UserResponse.model_validate(u) for u in users],
        total=total, page=page, per_page=per_page, total_pages=ceil(total / per_page),
    )


@router.post("", response_model=UserResponse, status_code=201)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN)),
):
    service = UserService(db)
    user = await service.create(data, current_user.id)
    return UserResponse.model_validate(user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN)),
):
    service = UserService(db)
    user = await service.get_by_id(user_id)
    return UserResponse.model_validate(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: uuid.UUID,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN)),
):
    service = UserService(db)
    user = await service.update(user_id, data)
    return UserResponse.model_validate(user)


@router.delete("/{user_id}", response_model=MessageResponse)
async def deactivate_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN)),
):
    service = UserService(db)
    await service.deactivate(user_id)
    return MessageResponse(message="User deactivated")
