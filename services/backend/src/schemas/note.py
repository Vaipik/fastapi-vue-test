from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, validator

from constants import note as constants


class NoteBase(BaseModel):
    title: str
    content: str

    @validator("title")
    def title_length(cls, v) -> None:
        len_v = len(v)
        if len_v < constants.TITLE_MIN_LENGTH:
            error_msg = f"Title length must be longer than {constants.TITLE_MIN_LENGTH}"
            raise ValueError(error_msg)

        if len_v > constants.TITLE_MAX_LENGTH:
            error_msg = f"Title length must be shorter than {constants.TITLE_MAX_LENGTH}"
            raise ValueError(error_msg)

    @validator("content")
    def content_length(cls, v) -> None:
        len_v = len(v)
        if len_v == constants.CONTENT_MIN_LENGTH:  # len_v = 0
            error_msg = "Note content can not be empty!"
            raise ValueError(error_msg)

        if len_v > constants.CONTENT_MAX_LENGTH:
            error_msg = f"Note content must be shorter than {constants.CONTENT_MAX_LENGTH}"
            raise ValueError(error_msg)


class NoteUpdate(BaseModel):
    id: UUID


class NoteResponse(NoteBase):
    id: UUID
    created_at: datetime
    edited_at: Optional[datetime]

    class Config:
        orm_mode = True
