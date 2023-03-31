from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from dependecies.database import get_repository
from repository.note import NoteRepository
from repository.user import UserRepository
from schemas.note import NoteResponse, NoteBase, NoteUpdate

notes_api = APIRouter(
    prefix="/notes",
    tags=["notes"]
)


@notes_api.get(
    "/",
    response_model=List[NoteResponse]
)
async def get_user_notes(
        note_repo: NoteRepository = Depends(get_repository(NoteRepository)),
        user_repo: UserRepository = Depends(get_repository(UserRepository))
):
    user_email = "email@com.ua"
    user = await user_repo.get_user_by_email(user_email)
    notes = await note_repo.get_user_notes(user)
    return notes


@notes_api.post(
    "/",
    response_model=NoteResponse
)
async def create_user_note(
        note_data: NoteBase,
        note_repo: NoteRepository = Depends(get_repository(NoteRepository)),
        user_repo: UserRepository = Depends(get_repository(UserRepository))
):
    user_email = "email@com.ua"
    user = await user_repo.get_user_by_email(user_email)
    note = await note_repo.create_note(note_data, user)
    return note


@notes_api.put(
    "/{note_id}",
    response_model=NoteResponse
)
async def update_user_note(
        note_data: NoteBase,
        note_id: UUID,
        note_repo: NoteRepository = Depends(get_repository(NoteRepository)),
):
    note = await note_repo.update_note(note_id, note_data)
    return note
