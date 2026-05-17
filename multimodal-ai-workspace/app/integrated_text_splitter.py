from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import get_settings


class IntegratedTextSplitter:
    """
    Split integrated RAG documents into smaller chunks.
    """

    def __init__(
        self,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ) -> None:
        settings = get_settings()

        self.chunk_size = chunk_size or settings.rag_chunk_size
        self.chunk_overlap = (
            chunk_overlap
            if chunk_overlap is not None
            else settings.rag_chunk_overlap
        )

        self._validate_settings()

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def split_documents(
        self,
        documents: list[Document],
    ) -> list[Document]:
        """
        Split documents and enrich chunk metadata.
        """
        if not documents:
            return []

        chunks = self.splitter.split_documents(documents)

        for index, chunk in enumerate(chunks, start=1):
            chunk.metadata = {
                **chunk.metadata,
                "chunk_id": index,
                "chunk_size": len(chunk.page_content),
            }

        return chunks

    def _validate_settings(self) -> None:
        """
        Validate chunking settings.
        """
        if self.chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0.")

        if self.chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative.")

        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )