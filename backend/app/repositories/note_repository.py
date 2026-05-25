from typing import Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.note import Note
from app.models.user import User


class NoteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_note_by_id(self, note_id: int) -> Optional[Note]:
        """
        Return a note from the db that matches the passed in note id.
        """
        return await self.session.get(Note, note_id)

    async def get_note_by_author_id(self, author_id: int) -> Optional[Note]:
        """
        Find and return a note that matches the passed in author id.
        """
        q = select(Note).where(Note.author_id == author_id)
        result = await self.session.execute(q)
        return result.scalars().first()

    async def get_note_by_author_username(self, author_username: str) -> Optional[Note]:
        """
        Find and return a note that matches the passed in author username.
        """
        q = select(Note).join(User).where(User.username == author_username)
        result = await self.session.execute(q)
        return result.scalars().first()

    async def add_note(self, note: Note) -> Note:
        """
        Add a new note to the database.
        """
        self.session.add(note)
        await self.session.flush()
        return note

    async def update_note_embedding(self, note: Note, embedding: Vector) -> Note:
        """
        Save the note vector embedding to the database.
        """
        note.embedding = embedding
        await self.session.flush()
        return note

    async def update(self, note: Note, **fields) -> Note:
        """
        Update an existing note in the database with the passed in fields.
        """
        for k, v in fields.items():
            setattr(note, k, v)
        await self.session.flush()
        return note

    async def delete(self, note: Note) -> None:
        """
        Delete a note from the database.
        """
        await self.session.delete(note)
        await self.session.flush()
