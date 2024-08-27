from datetime import datetime

from pydantic import BaseModel


class BaseNote(BaseModel):
    title: str
    content: str | None = None


class CreateNote(BaseNote):
    pass


class Note(BaseNote):
    id: int
    created_at: datetime
