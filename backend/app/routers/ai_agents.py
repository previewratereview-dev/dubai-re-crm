import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.user import User, UserRole
from app.schemas.ai_agent import AIAgentCreate, AIAgentUpdate, AIAgentResponse
from app.schemas.common import PaginatedResponse, MessageResponse
from app.services.ai_agent import AIAgentService
from math import ceil

router = APIRouter(prefix="/api/ai-agents", tags=["AI Agents"])


@router.get("", response_model=PaginatedResponse)
async def list_agents(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AIAgentService(db)
    agents, total = await service.get_all(page, per_page)
    return PaginatedResponse(
        items=[AIAgentResponse.model_validate(a) for a in agents],
        total=total, page=page, per_page=per_page, total_pages=ceil(total / per_page),
    )


@router.post("", response_model=AIAgentResponse, status_code=201)
async def create_agent(
    data: AIAgentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.DEVELOPER)),
):
    service = AIAgentService(db)
    agent = await service.create(data)
    return AIAgentResponse.model_validate(agent)


@router.get("/{agent_id}", response_model=AIAgentResponse)
async def get_agent(
    agent_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AIAgentService(db)
    agent = await service.get_by_id(agent_id)
    return AIAgentResponse.model_validate(agent)


@router.put("/{agent_id}", response_model=AIAgentResponse)
async def update_agent(
    agent_id: uuid.UUID,
    data: AIAgentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.DEVELOPER)),
):
    service = AIAgentService(db)
    agent = await service.update(agent_id, data)
    return AIAgentResponse.model_validate(agent)


@router.delete("/{agent_id}", response_model=MessageResponse)
async def delete_agent(
    agent_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN)),
):
    service = AIAgentService(db)
    await service.delete(agent_id)
    return MessageResponse(message="Agent deleted")
