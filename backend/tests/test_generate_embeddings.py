import pytest

from app.core.dependencies import generate_embeddings


@pytest.mark.asyncio
async def test_generate_embeddings_returns_vector():
    """Integration test: verify real embeddings are generated."""

    embedding = await generate_embeddings("Hello world", "This is test content")

    assert embedding is not None
    assert isinstance(embedding, list)
    assert len(embedding) == 384


@pytest.mark.asyncio
async def test_generate_embeddings_deterministic():
    """Integration test: same input produces same embedding."""

    embedding1 = await generate_embeddings("Test content", "More content")
    embedding2 = await generate_embeddings("Test content", "More content")

    assert embedding1 == embedding2
