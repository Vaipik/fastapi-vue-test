from typing import Optional, Sequence
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy import func

from .base import BaseRepository
from models.user import User
from models.note import Note
from schemas.note import NoteBase


class NoteRepository(BaseRepository):

    async def get_user_notes(self, user: User) -> Sequence[Optional[Note]]:
        stmt = sa.select(Note).where(Note.user == user)
        notes = await self._session.execute(stmt)
        return notes.scalars().all()

    async def get_note_by_id(self, note_id: UUID) -> Optional[Note]:
        note = await self._session.get(Note, note_id)
        return note

    async def create_note(self, body: NoteBase, user: User) -> Note:
        note = Note(
            **body.dict(),
            user=user
        )
        self._session.add(note)
        await self._session.commit()
        await self._session.refresh(instance=note)
        return note

    async def update_note(self, note_id: UUID, body: NoteBase) -> Optional[Note]:
        note = await self.get_note_by_id(note_id)
        if note is None:
            pass  # TODO: Raise Error
        is_updated = False
        note_data = body.dict()
        update_stmt = sa.update(Note).where(Note.id == note_id)

        if note_data["title"]:
            update_stmt = update_stmt.values(title=note_data["title"])
            is_updated = True

        if note_data["content"]:
            update_stmt = update_stmt.values(content=note_data["content"])
            is_updated = True

        if is_updated:
            await self._session.execute(update_stmt)
            await self._session.commit()
            await self._session.refresh(instance=note)
            return note

    async def delete_note(self, note_id: UUID) -> None:
        note = await self.get_note_by_id(note_id)
        if note is None:
            pass  # TODO: Raise Error

        stmt = sa.delete(Note).where(Note.id == note_id)
        await self._session.execute(stmt)
        await self._session.commit()
