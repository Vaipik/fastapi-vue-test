from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

"""
    title: Mapped[str] = mapped_column(
        String(constants.TITLE_MAX_LENGTH)
    )
    content: Mapped[str] = mapped_column(
        String(constants.CONTENT_MAX_LENGTH)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=datetime.utcnow
    )
    edited_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, onupdate=datetime.utcnow
    )
"""


class NoteBase(BaseModel):
    title: str
    content: str


class NoteUpdate(BaseModel):
    id: UUID


class NoteResponse(NoteBase):
    id: UUID
    created_at: datetime
    edited_at: Optional[datetime]

    class Config:
        orm_mode = True
