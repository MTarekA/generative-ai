from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import get_settings


class DocumentTextSplitter:
    """
    Split loaded documents into smaller chunks.

    Chunking is a critical step in RAG systems because retrieval quality
    depends heavily on how the source documents are divided.
    """

    def __init__(
        self,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ) -> None:
        settings = get_settings()

        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap

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
        Split documents into chunks and preserve metadata.

        Each generated chunk keeps the original metadata, then receives
        additional chunk-specific metadata.
        """
        if not documents:
            raise ValueError("No documents provided for splitting.")

        chunks = self.splitter.split_documents(documents)

        for index, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = index
            chunk.metadata["chunk_size"] = len(chunk.page_content)

        return chunks


if __name__ == "__main__":
    from app.document_loader import DocumentLoader

    loader = DocumentLoader()
    documents = loader.load_documents()

    splitter = DocumentTextSplitter()
    chunks = splitter.split_documents(documents)

    print(f"Original documents: {len(documents)}")
    print(f"Generated chunks: {len(chunks)}")
    print("First chunk metadata:", chunks[0].metadata)
    print("First chunk preview:")
    print(chunks[0].page_content[:500])