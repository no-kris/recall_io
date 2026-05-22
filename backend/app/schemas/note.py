from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field


class NoteCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=50)
    content: str = Field(
        ..., max_length=10000, json_schema_extra={"widget": "textarea"}
    )


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=5, max_length=50)
    content: Optional[str] = Field(
        default=None, max_length=10000, json_schema_extra={"widget": "textarea"}
    )


class NotePublic(BaseModel):
    id: int
    author_id: int
    title: str
    content: str

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def blurb(self) -> str:
        """Returns a 50-character preview of the content."""
        if len(self.content) > 50:
            return f"{self.content[:50]}..."
        return self.content
