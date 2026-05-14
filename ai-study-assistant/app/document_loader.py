from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

from app.config import RAW_DATA_DIR


SUPPORTED_EXTENSIONS = {".pdf", ".txt"}


class DocumentLoader:
    """
    Load supported lecture files from the raw data directory.

    Supported formats:
    - PDF files using PyPDFLoader
    - TXT files using TextLoader

    The output is a list of LangChain Document objects.
    Each document contains:
    - page_content: the extracted text
    - metadata: source information such as file name and page number
    """

    def __init__(self, raw_data_dir: Path | None = None) -> None:
        self.raw_data_dir = raw_data_dir or RAW_DATA_DIR

    def load_documents(self) -> list[Document]:
        """
        Load all supported documents from the raw data directory.
        """
        self._ensure_raw_data_dir_exists()

        files = self._get_supported_files()

        if not files:
            raise FileNotFoundError(
                f"No supported files found in: {self.raw_data_dir}. "
                f"Supported extensions: {SUPPORTED_EXTENSIONS}"
            )

        documents: list[Document] = []

        for file_path in files:
            loaded_docs = self._load_single_file(file_path)
            documents.extend(loaded_docs)

        return documents

    def _ensure_raw_data_dir_exists(self) -> None:
        """
        Ensure that the raw data directory exists before reading files.
        """
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)

    def _get_supported_files(self) -> list[Path]:
        """
        Return all supported files from the raw data directory.
        """
        files = []

        for path in self.raw_data_dir.iterdir():
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
                files.append(path)

        return sorted(files)

    def _load_single_file(self, file_path: Path) -> list[Document]:
        """
        Load a single file based on its extension.
        """
        suffix = file_path.suffix.lower()

        if suffix == ".pdf":
            return self._load_pdf(file_path)

        if suffix == ".txt":
            return self._load_txt(file_path)

        raise ValueError(f"Unsupported file type: {file_path.suffix}")

    def _load_pdf(self, file_path: Path) -> list[Document]:
        """
        Load a PDF file and enrich its metadata.
        """
        loader = PyPDFLoader(str(file_path))
        documents = loader.load()

        for doc in documents:
            doc.metadata["source"] = str(file_path)
            doc.metadata["file_name"] = file_path.name
            doc.metadata["file_type"] = "pdf"

        return documents

    def _load_txt(self, file_path: Path) -> list[Document]:
        """
        Load a TXT file and enrich its metadata.
        """
        loader = TextLoader(
            str(file_path),
            encoding="utf-8",
            autodetect_encoding=True,
        )
        documents = loader.load()

        for doc in documents:
            doc.metadata["source"] = str(file_path)
            doc.metadata["file_name"] = file_path.name
            doc.metadata["file_type"] = "txt"

        return documents


if __name__ == "__main__":
    loader = DocumentLoader()
    docs = loader.load_documents()

    print(f"Loaded documents: {len(docs)}")
    print("First document metadata:", docs[0].metadata)
    print("First document preview:")
    print(docs[0].page_content[:500])