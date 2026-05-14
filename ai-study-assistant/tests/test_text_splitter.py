from langchain_core.documents import Document

from app.text_splitter import DocumentTextSplitter


def test_text_splitter_creates_chunks() -> None:
    """
    Test that DocumentTextSplitter creates chunks and preserves metadata.
    """
    document = Document(
        page_content=(
            "Generative AI is useful for text, image, audio, and code. "
            "RAG systems combine retrieval with generation. "
            "Embeddings help represent semantic meaning."
        ),
        metadata={"file_name": "lecture.txt", "file_type": "txt"},
    )

    splitter = DocumentTextSplitter(
        chunk_size=80,
        chunk_overlap=20,
    )

    chunks = splitter.split_documents([document])

    assert len(chunks) >= 1
    assert "chunk_id" in chunks[0].metadata
    assert "chunk_size" in chunks[0].metadata
    assert chunks[0].metadata["file_name"] == "lecture.txt"