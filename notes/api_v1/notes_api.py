from fastapi import APIRouter, Depends, status
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth import get_auth_user_username
from database.db import get_db_session
from database.models import NoteModel
from schemas import CreateNote, Note
from validation.note_validation import validate_note


router = APIRouter(prefix='/notes', tags=['Notes'])


@router.get('/', response_model=list[Note])
async def get_notes_list(
    db_session: AsyncSession = Depends(get_db_session),
    username: str = Depends(get_auth_user_username)
):
    stmt = select(NoteModel).where(NoteModel.username==username).order_by(NoteModel.created_at)
    result: Result = await db_session.execute(stmt)
    notes = result.scalars().all()
    return notes


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_new_note(
    raw_note: CreateNote,
    db_session: AsyncSession = Depends(get_db_session),
    username: str = Depends(get_auth_user_username)
):
    validated_raw_note = await validate_note(raw_note)
    note = NoteModel(username=username, **validated_raw_note.model_dump())
    db_session.add(note)
    await db_session.commit()
    return {'status': 'success', 'message': 'Note created successfully'}
