from app.core.dependencies import generate_embeddings
from app.core.exceptions import (
    MissingNeededValuesError,
    NoteNotFoundError,
)
from app.models.note import Note
from app.repositories.note_repository import NoteRepository


class NoteService:
    def __init__(self, repository: NoteRepository) -> None:
        self.repository = repository

    async def get_note(self, note_id: int):
        """
        Return a note matching the note id parameter.
        """
        note = await self.repository.get_note_by_id(note_id)
        if not note:
            raise NoteNotFoundError("Note does not exist.")

        return note

    async def create_note(self, author_id: int, title: str, content: str) -> Note:
        """
        Create a new note and generate the vector embedding for it.
        """
        if not title or not content:
            raise MissingNeededValuesError("Check for missing values.")

        embedding = await generate_embeddings(title, content)
        note = Note(
            title=title, content=content, author_id=author_id, embedding=embedding
        )
        return await self.repository.add_note(note)

    async def update_note(self, note_id: int, **fields) -> Note:
        """
        Update note information, including vector embedding.
        Raises NoteNotFoundError if note does not exists.
        """
        note = await self.repository.get_note_by_id(note_id)
        if not note:
            raise NoteNotFoundError("Note does not exist.")

        note = await self.repository.update(note, **fields)
        if "title" in fields or "content" in fields:
            title = fields.get("title", note.title)
            content = fields.get("content", note.content)
            embedding = await generate_embeddings(title, content)
            note = await self.repository.update_note_embedding(note, embedding)

        return note

    async def delete_note(self, note_id: int) -> None:
        """
        Delete a note that matches the note id paramater.
        Raises NoteNotFoundError if note does not exists.
        """
        deleted_note = await self.repository.get_note_by_id(note_id)
        if not deleted_note:
            raise NoteNotFoundError("Note does not exist.")

        await self.repository.delete(deleted_note)
