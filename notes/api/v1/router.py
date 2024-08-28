from fastapi import APIRouter, Depends, status
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db_session
from database.models import NoteModel
from validators import validate_note
from schemas import CreateNote, Note


router = APIRouter(prefix='/api/v1', tags=['Notes'])

@router.get('/notes', response_model=list[Note])
async def get_notes_list(db_session: AsyncSession = Depends(get_db_session)):
    stmt = select(NoteModel).order_by(NoteModel.created_at)
    result: Result = await db_session.execute(stmt)
    notes = result.scalars().all()
    return notes

@router.post('/notes', status_code=status.HTTP_201_CREATED)
async def create_new_note(
    raw_note: CreateNote,
    db_session: AsyncSession = Depends(get_db_session)
):
    validated_raw_note = await validate_note(raw_note)
    note = NoteModel(**validated_raw_note.model_dump())
    db_session.add(note)
    await db_session.commit()
    return {'status': 'success', 'message': 'Note created successfully'}
