from pathlib import Path

from app.document_loader import DocumentLoader


def test_document_loader_loads_txt_file(tmp_path: Path) -> None:
    """
    Test that DocumentLoader can load a TXT file correctly.
    """
    test_file = tmp_path / "lecture.txt"
    test_file.write_text(
        "Retrieval-Augmented Generation combines retrieval and generation.",
        encoding="utf-8",
    )

    loader = DocumentLoader(raw_data_dir=tmp_path)
    documents = loader.load_documents()

    assert len(documents) == 1
    assert "Retrieval-Augmented Generation" in documents[0].page_content
    assert documents[0].metadata["file_name"] == "lecture.txt"
    assert documents[0].metadata["file_type"] == "txt"