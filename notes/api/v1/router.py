from fastapi import APIRouter, status

from schemas import CreateNote, Note


router = APIRouter(prefix='/api/v1', tags=['Notes'])

@router.get('/notes', response_model=list[Note])
async def get_notes_list():
    notes = get_notes()
    return notes

@router.post('/notes', status_code=status.HTTP_201_CREATED)
async def create_new_note(raw_note: CreateNote):
    note = validate_note(raw_note)
    create_note(note)
    return {'status': 'success', 'message': 'Note created successfully'}
