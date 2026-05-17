from pathlib import Path

import pytest

from app.integrated_document_loader import IntegratedDocumentLoader


def test_integrated_document_loader_lists_supported_files(
    tmp_path: Path,
) -> None:
    """
    Test that the document loader lists only supported PDF/TXT files.
    """
    txt_file = tmp_path / "notes.txt"
    txt_file.write_text("This is a test document.", encoding="utf-8")

    unsupported_file = tmp_path / "image.png"
    unsupported_file.write_bytes(b"fake image")

    loader = IntegratedDocumentLoader(documents_dir=tmp_path)
    files = loader.list_document_files()

    assert len(files) == 1
    assert files[0].file_name == "notes.txt"
    assert files[0].file_extension == ".txt"


def test_integrated_document_loader_loads_txt_file(
    tmp_path: Path,
) -> None:
    """
    Test loading a TXT file as a LangChain document.
    """
    txt_file = tmp_path / "rag_notes.txt"
    txt_file.write_text(
        "Retrieval-Augmented Generation combines retrieval and generation.",
        encoding="utf-8",
    )

    loader = IntegratedDocumentLoader(documents_dir=tmp_path)
    documents = loader.load_documents()

    assert len(documents) == 1
    assert "Retrieval-Augmented Generation" in documents[0].page_content
    assert documents[0].metadata["file_name"] == "rag_notes.txt"
    assert documents[0].metadata["file_type"] == ".txt"


def test_integrated_document_loader_returns_empty_for_empty_txt(
    tmp_path: Path,
) -> None:
    """
    Test that empty TXT files do not produce documents.
    """
    txt_file = tmp_path / "empty.txt"
    txt_file.write_text("   ", encoding="utf-8")

    loader = IntegratedDocumentLoader(documents_dir=tmp_path)
    documents = loader.load_documents()

    assert documents == []


def test_integrated_document_loader_rejects_missing_file(
    tmp_path: Path,
) -> None:
    """
    Test that missing document files raise FileNotFoundError.
    """
    missing_file = tmp_path / "missing.txt"

    loader = IntegratedDocumentLoader(documents_dir=tmp_path)

    with pytest.raises(FileNotFoundError):
        loader.load_single_document(missing_file)


def test_integrated_document_loader_rejects_unsupported_file(
    tmp_path: Path,
) -> None:
    """
    Test that unsupported file types are rejected.
    """
    unsupported_file = tmp_path / "notes.docx"
    unsupported_file.write_text("Unsupported document.", encoding="utf-8")

    loader = IntegratedDocumentLoader(documents_dir=tmp_path)

    with pytest.raises(ValueError, match="Unsupported document type"):
        loader.load_single_document(unsupported_file)