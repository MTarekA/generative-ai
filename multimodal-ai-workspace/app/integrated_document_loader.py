from dataclasses import dataclass
from pathlib import Path

from langchain_core.documents import Document
from pypdf import PdfReader

from app.config import INTEGRATED_DOCUMENTS_DIR


SUPPORTED_DOCUMENT_EXTENSIONS = {
    ".pdf",
    ".txt",
}


@dataclass
class IntegratedDocumentFile:
    """
    Structured representation of an integrated RAG document file.
    """

    file_path: Path
    file_name: str
    file_extension: str
    file_size_bytes: int


class IntegratedDocumentLoader:
    """
    Load PDF and TXT documents for the integrated RAG demo.
    """

    def __init__(
        self,
        documents_dir: Path | None = None,
        supported_extensions: set[str] | None = None,
    ) -> None:
        self.documents_dir = documents_dir or INTEGRATED_DOCUMENTS_DIR
        self.supported_extensions = (
            supported_extensions or SUPPORTED_DOCUMENT_EXTENSIONS
        )

    def list_document_files(self) -> list[IntegratedDocumentFile]:
        """
        Return supported document files from the integrated documents folder.
        """
        if not self.documents_dir.exists():
            return []

        files = []

        for path in sorted(self.documents_dir.iterdir()):
            if not path.is_file():
                continue

            extension = path.suffix.lower()

            if extension not in self.supported_extensions:
                continue

            files.append(
                IntegratedDocumentFile(
                    file_path=path,
                    file_name=path.name,
                    file_extension=extension,
                    file_size_bytes=path.stat().st_size,
                )
            )

        return files

    def load_documents(self) -> list[Document]:
        """
        Load all supported documents from the integrated documents folder.
        """
        documents = []

        for document_file in self.list_document_files():
            if document_file.file_extension == ".pdf":
                documents.extend(self._load_pdf(document_file.file_path))

            elif document_file.file_extension == ".txt":
                documents.extend(self._load_txt(document_file.file_path))

        return documents

    def load_single_document(self, file_path: str | Path) -> list[Document]:
        """
        Load one supported document.
        """
        path = Path(file_path)
        self._validate_document_path(path)

        extension = path.suffix.lower()

        if extension == ".pdf":
            return self._load_pdf(path)

        if extension == ".txt":
            return self._load_txt(path)

        raise ValueError(f"Unsupported document type: {extension}")

    def _load_pdf(self, file_path: Path) -> list[Document]:
        """
        Load PDF pages as LangChain Document objects.
        """
        self._validate_document_path(file_path)

        reader = PdfReader(str(file_path))
        documents = []

        for page_index, page in enumerate(reader.pages):
            text = page.extract_text() or ""

            if not text.strip():
                continue

            documents.append(
                Document(
                    page_content=text.strip(),
                    metadata={
                        "file_name": file_path.name,
                        "file_type": ".pdf",
                        "source": str(file_path),
                        "page": page_index + 1,
                    },
                )
            )

        return documents

    def _load_txt(self, file_path: Path) -> list[Document]:
        """
        Load a TXT file as one LangChain Document object.
        """
        self._validate_document_path(file_path)

        text = file_path.read_text(encoding="utf-8")

        if not text.strip():
            return []

        return [
            Document(
                page_content=text.strip(),
                metadata={
                    "file_name": file_path.name,
                    "file_type": ".txt",
                    "source": str(file_path),
                    "page": None,
                },
            )
        ]

    def _validate_document_path(self, file_path: Path) -> None:
        """
        Validate that a document path exists and is supported.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")

        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")

        extension = file_path.suffix.lower()

        if extension not in self.supported_extensions:
            raise ValueError(
                f"Unsupported document type: {extension}. "
                f"Supported types: {self.supported_extensions}"
            )