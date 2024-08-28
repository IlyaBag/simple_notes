from schemas import CreateNote


async def validate_note(note: CreateNote) -> CreateNote:
    return note
