import pytest

from app.rag_pipeline import RAGPipeline


def test_rag_pipeline_rejects_empty_question_without_initializing() -> None:
    """
    Test the empty-question validation logic without calling external APIs.

    We bypass __init__ because this test only checks local validation
    inside the ask method.
    """
    pipeline = object.__new__(RAGPipeline)

    with pytest.raises(ValueError, match="Question cannot be empty"):
        pipeline.ask("   ")