import pytest
from langchain_core.documents import Document

from app.integrated_text_splitter import IntegratedTextSplitter


def test_integrated_text_splitter_splits_documents() -> None:
    """
    Test that documents are split into chunks with metadata.
    """
    documents = [
        Document(
            page_content=(
                "Retrieval-Augmented Generation combines retrieval "
                "with text generation. It helps ground answers in "
                "external documents."
            ),
            metadata={
                "file_name": "test.txt",
                "file_type": ".txt",
                "source": "test.txt",
                "page": None,
            },
        )
    ]

    splitter = IntegratedTextSplitter(
        chunk_size=50,
        chunk_overlap=10,
    )

    chunks = splitter.split_documents(documents)

    assert len(chunks) >= 1
    assert "chunk_id" in chunks[0].metadata
    assert "chunk_size" in chunks[0].metadata
    assert chunks[0].metadata["file_name"] == "test.txt"


def test_integrated_text_splitter_returns_empty_list_for_empty_input() -> None:
    """
    Test empty document input.
    """
    splitter = IntegratedTextSplitter(
        chunk_size=50,
        chunk_overlap=10,
    )

    chunks = splitter.split_documents([])

    assert chunks == []


def test_integrated_text_splitter_rejects_invalid_overlap() -> None:
    """
    Test invalid chunk overlap.
    """
    with pytest.raises(ValueError, match="chunk_overlap must be smaller"):
        IntegratedTextSplitter(
            chunk_size=100,
            chunk_overlap=100,
        )