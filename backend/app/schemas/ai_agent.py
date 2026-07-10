import uuid
from datetime import datetime
from pydantic import BaseModel
from app.models.ai_agent import AgentStatus


class AIAgentCreate(BaseModel):
    name: str
    agent_id: str
    description: str | None = None
    purpose: str | None = None
    language: str = "en"
    phone_number: str | None = None
    status: AgentStatus = AgentStatus.ACTIVE
    knowledge_sources: list = []
    prompt_version: str | None = None


class AIAgentUpdate(BaseModel):
    name: str | None = None
    agent_id: str | None = None
    description: str | None = None
    purpose: str | None = None
    language: str | None = None
    phone_number: str | None = None
    status: AgentStatus | None = None
    knowledge_sources: list | None = None
    prompt_version: str | None = None


class AIAgentResponse(BaseModel):
    id: uuid.UUID
    name: str
    agent_id: str
    description: str | None
    purpose: str | None
    language: str
    phone_number: str | None
    status: AgentStatus
    knowledge_sources: list | None
    prompt_version: str | None
    last_updated: datetime | None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
