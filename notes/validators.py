import json
from typing import Any
import httpx

from schemas import CreateNote


CHECKER_URL = 'https://speller.yandex.net/services/spellservice.json/checkTexts'


async def validate_note(note: CreateNote) -> CreateNote:
    """
    Receives a note and checks the text in its fields for errors. Returns a 
    new note object with the errors corrected.
    """
    texts_corrections = await get_corrections((note.title, note.content or ''))
    note_title_corrections = texts_corrections[0]
    note_content_corrections = texts_corrections[1]

    corrected_note_title = fix_mistakes(note.title, note_title_corrections)
    corrected_note_content = fix_mistakes(note.content or '',
                                          note_content_corrections)

    validated_note = CreateNote(
        title=corrected_note_title,
        content=corrected_note_content
    )
    return validated_note

async def get_corrections(texts: tuple[str, str]) -> list:
    """
    Checks given texts (array of strings) with Yandex Speller API.

    Example of texts:
    ("string nomber onne", "string is a chsrs array")
    
    Example of API response:
    [
      [
        {
            'code': 1,
            'pos': 7,
            'row': 0,
            'col': 7,
            'len': 6,
            'word': 'nomber',
            's': ['number', 'nomber']
        },
        {
          'code': 1,
          'pos': 14,
          'row': 0,
          'col': 14,
          'len': 4,
          'word': 'onne',
          's': ['one', 'none']
        }
      ],
      [
        {
          'code': 1,
          'pos': 12,
          'row': 0,
          'col': 12,
          'len': 5,
          'word': 'chsrs',
          's': ['chars', 'char', 'chats']
        }
      ]
    ]
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url=CHECKER_URL, params={'text': texts})
    response.raise_for_status()
    return json.loads(response.text)

def fix_mistakes(source_text: str, corrections: list[dict[str, Any]]) -> str:
    """Corrects mistakes in given text using the correction list."""
    if len(corrections) == 0:
        return source_text
    corrected_text = ''
    prev_end_pos = 0
    for mistake in corrections:
        start_pos = mistake['pos']
        end_pos = start_pos + mistake['len']
        corrected_text += source_text[prev_end_pos:start_pos] + mistake['s'][0]
        prev_end_pos = end_pos
    return corrected_text
