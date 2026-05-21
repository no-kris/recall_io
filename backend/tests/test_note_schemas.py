import pytest

from app.schemas.note import NoteCreate, NotePublic, NoteUpdate


# Mock the SQLAlchemy model
class MockNote:
    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content


@pytest.mark.parametrize(
    "content, expected_blurb",
    [
        ("Short content", "Short content"),  # Normal
        ("a" * 100, "a" * 50 + "..."),  # Long one-liner
    ],
)
def test_note_public_blurb_generation(content, expected_blurb):
    mock = MockNote(id=1, title="Test Title", content=content)
    public = NotePublic.model_validate(mock)
    assert public.blurb == expected_blurb


@pytest.mark.parametrize(
    "schema_class, title, content, is_valid",
    [
        (NoteCreate, "Valid Title", "Valid Content", True),
        (NoteCreate, "Shor", "Valid Content", False),  # Title < 5
        (NoteUpdate, None, None, True),  # Optional fields
        (NoteUpdate, "New Title", None, True),  # Partial update
    ],
)
def test_note_schema_validation(schema_class, title, content, is_valid):
    if is_valid:
        schema_class(title=title, content=content)
    else:
        with pytest.raises(Exception):
            schema_class(title=title, content=content)
