import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.schemas.common import MessageResponse
from app.services.note import NoteService

router = APIRouter(prefix="/api/notes", tags=["Notes"])


@router.get("/lead/{lead_id}", response_model=list[NoteResponse])
async def get_lead_notes(
    lead_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NoteService(db)
    notes = await service.get_by_lead(lead_id)
    return [NoteResponse.model_validate(n) for n in notes]


@router.get("/customer/{customer_id}", response_model=list[NoteResponse])
async def get_customer_notes(
    customer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NoteService(db)
    notes = await service.get_by_customer(customer_id)
    return [NoteResponse.model_validate(n) for n in notes]


@router.post("", response_model=NoteResponse, status_code=201)
async def create_note(
    data: NoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NoteService(db)
    note = await service.create(data, current_user.id)
    return NoteResponse.model_validate(note)


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: uuid.UUID,
    data: NoteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NoteService(db)
    note = await service.update(note_id, data)
    if not note:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return NoteResponse.model_validate(note)


@router.delete("/{note_id}", response_model=MessageResponse)
async def delete_note(
    note_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NoteService(db)
    await service.delete(note_id)
    return MessageResponse(message="Note deleted")
