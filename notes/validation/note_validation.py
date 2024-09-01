from validation.speller_validator import correct_texts
from schemas import CreateNote


async def validate_note(note: CreateNote) -> CreateNote:
    """
    Receives a note and checks the text in its fields for errors. Returns a 
    new note object with the errors corrected.
    """
    note_fields = (note.title, note.content or '')
    validated_note_fields = await correct_texts(note_fields)

    validated_note = CreateNote(
        title=validated_note_fields[0],
        content=validated_note_fields[1],
    )
    return validated_note
