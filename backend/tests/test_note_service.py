# File: study-vault/backend/tests/test_note_service.py

from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import NoteNotFoundError
from app.models.note import Note
from app.services.note_service import NoteService


@pytest.fixture
def mock_note_repository():
    """Create a mock NoteRepository."""
    mock = AsyncMock()
    return mock


@pytest.fixture
def mock_generate_embeddings(monkeypatch):
    """Mock the generate_embeddings function."""
    mock = AsyncMock(return_value=[0.1] * 384)
    monkeypatch.setattr("app.services.note_service.generate_embeddings", mock)
    return mock


@pytest.mark.asyncio
async def test_create_note_success(mock_note_repository, mock_generate_embeddings):
    """Test successfully creating a note."""
    note = Note(id=1, author_id=1, title="Test", content="Content")
    mock_note_repository.add_note.return_value = note

    service = NoteService(mock_note_repository)
    result = await service.create_note(1, "Test", "Content")

    assert result == note


@pytest.mark.asyncio
async def test_update_note_raises_error_if_not_found(mock_note_repository):
    """Test that updating a non-existent note raises NoteNotFoundError."""
    mock_note_repository.get_note_by_id.return_value = None
    service = NoteService(mock_note_repository)

    with pytest.raises(NoteNotFoundError):
        await service.update_note(999, title="New Title")


@pytest.mark.asyncio
async def test_delete_note_raises_error_if_not_found(mock_note_repository):
    """Test that deleting a non-existent note raises NoteNotFoundError."""
    mock_note_repository.get_note_by_id.return_value = None
    service = NoteService(mock_note_repository)

    with pytest.raises(NoteNotFoundError):
        await service.delete_note(999)
