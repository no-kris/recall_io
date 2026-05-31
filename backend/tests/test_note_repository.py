import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.note import Note
from app.models.user import User
from app.repositories.note_repository import NoteRepository


@pytest.mark.asyncio
async def test_get_note_by_id(
    note_repository: NoteRepository, test_db_session: AsyncSession
):
    note = Note(id=1, author_id=1, title="test note", content="this is a test note")
    test_db_session.add(note)
    await test_db_session.flush()

    result = await note_repository.get_note_by_id(note.id)

    assert result is not None
    assert result.title == note.title
    assert result.content == note.content


@pytest.mark.asyncio
async def test_get_note_by_author_id(
    note_repository: NoteRepository, test_db_session: AsyncSession
):
    note = Note(id=2, author_id=2, title="test note", content="this is a test note")
    test_db_session.add(note)
    await test_db_session.flush()

    result = await note_repository.get_note_by_author_id(note.author_id)

    assert result is not None
    assert result.title == note.title
    assert result.content == note.content


@pytest.mark.asyncio
async def test_get_note_by_author_username(
    note_repository: NoteRepository, test_db_session: AsyncSession
):
    user = User(
        id=1,
        username="john_doe",
        email="john@example.com",
        auth_provider_id="auth_john_123",
    )
    test_db_session.add(user)
    await test_db_session.flush()

    note = Note(
        id=10,
        author_id=user.id,
        title="My First Note",
        content="This is a note by john_doe",
    )
    test_db_session.add(note)
    await test_db_session.flush()

    result = await note_repository.get_note_by_author_username(user.username)

    assert result is not None
    assert result.title == note.title
    assert result.content == note.content


@pytest.mark.asyncio
async def test_update_note_with_embedding(
    note_repository: NoteRepository, test_db_session: AsyncSession
):
    note = Note(id=5, author_id=5, title="test note", content="this is a test note")
    test_db_session.add(note)
    await test_db_session.flush()

    fake_embedding = [0.1] * 384

    updated = await note_repository.update_note_embedding(note, fake_embedding)

    assert updated.embedding is not None
    assert len(updated.embedding) == 384  # type:ignore


@pytest.mark.asyncio
async def test_update_note(
    note_repository: NoteRepository, test_db_session: AsyncSession
):
    note = Note(id=3, author_id=3, title="test note", content="this is a test note")
    test_db_session.add(note)
    await test_db_session.flush()

    update = await note_repository.update(
        note, title="New Title", content="Updated content"
    )

    assert update is not None
    assert update.title == note.title
    assert update.content == note.content


@pytest.mark.asyncio
async def test_delete_note(
    note_repository: NoteRepository, test_db_session: AsyncSession
):
    note = Note(id=3, author_id=3, title="test note", content="this is a test note")
    test_db_session.add(note)
    await test_db_session.flush()

    result = await note_repository.get_note_by_id(note.id)

    assert result is not None

    await note_repository.delete(note)

    deleted_result = await note_repository.get_note_by_id(note.id)

    assert deleted_result is None
