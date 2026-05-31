from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db, get_note_service
from app.core.exceptions import MissingNeededValuesError, NoteNotFoundError
from app.models.user import User
from app.schemas.note import NoteCreate, NotePublic, NoteUpdate
from app.services.note_service import NoteService

router = APIRouter(prefix="/notes")


@router.get("/{note_id}", response_model=NotePublic, tags=["Notes"])
async def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    service: NoteService = Depends(get_note_service),
):
    """
    API route for fetching a specific note.
    """
    note = await service.get_note(note_id)

    if note.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    return note


@router.post(
    "/create",
    response_model=NotePublic,
    status_code=status.HTTP_201_CREATED,
    tags=["Notes"],
)
async def create_note(
    note_data: NoteCreate,
    current_user: User = Depends(get_current_user),
    service: NoteService = Depends(get_note_service),
    session: AsyncSession = Depends(get_db),
):
    """
    API route for creating and storing note objects.
    """
    try:
        note = await service.create_note(
            author_id=current_user.id, title=note_data.title, content=note_data.content
        )
        await session.commit()
        return note
    except MissingNeededValuesError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{note_id}", response_model=NotePublic, tags=["Notes"])
async def update_note(
    note_id: int,
    note_data: NoteUpdate,
    current_user: User = Depends(get_current_user),
    service: NoteService = Depends(get_note_service),
    session: AsyncSession = Depends(get_db),
):
    """API route for updating a note object."""
    note = await service.get_note(note_id)
    if note.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    try:
        note = await service.update_note(note_id, **note_data.model_dump())
        await session.commit()
        return note
    except NoteNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Notes"])
async def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    service: NoteService = Depends(get_note_service),
    session: AsyncSession = Depends(get_db),
):
    """API route for deleting a note object."""
    note = await service.get_note(note_id)
    if note.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    try:
        await service.delete_note(note_id)
        await session.commit()
    except NoteNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
