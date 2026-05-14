from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings

from app.config import VECTOR_DB_DIR, get_settings, validate_settings


FAISS_INDEX_DIR = VECTOR_DB_DIR / "faiss_index"


class VectorStoreManager:
    """
    Manage embedding generation and FAISS vector store operations.

    Responsibilities:
    - Create embedding model
    - Build a FAISS vector index from document chunks
    - Save the index locally
    - Load an existing index
    - Return a retriever for semantic search
    """

    def __init__(self, index_dir: Path | None = None) -> None:
        self.settings = get_settings()
        validate_settings(self.settings)

        self.index_dir = index_dir or FAISS_INDEX_DIR
        self.embeddings = self._create_embeddings()

    def _create_embeddings(self):
        """
        Create the embedding model based on project settings.
        """
        if self.settings.embedding_provider == "openai":
            return OpenAIEmbeddings(
                model=self.settings.openai_embedding_model,
                api_key=self.settings.openai_api_key,
            )

        if self.settings.embedding_provider == "gemini":
            return GoogleGenerativeAIEmbeddings(
                model=self.settings.gemini_embedding_model,
                google_api_key=self.settings.google_api_key,
            )

        raise ValueError(
            f"Unsupported embedding provider: "
            f"{self.settings.embedding_provider}"
        )

    def build_vector_store(
        self,
        chunks: list[Document],
        save: bool = True,
    ) -> FAISS:
        """
        Build a FAISS vector store from document chunks.
        """
        if not chunks:
            raise ValueError("No chunks provided to build vector store.")

        vector_store = FAISS.from_documents(
            documents=chunks,
            embedding=self.embeddings,
        )

        if save:
            self.save_vector_store(vector_store)

        return vector_store

    def save_vector_store(self, vector_store: FAISS) -> None:
        """
        Save FAISS index locally.
        """
        self.index_dir.mkdir(parents=True, exist_ok=True)
        vector_store.save_local(str(self.index_dir))

    def load_vector_store(self) -> FAISS:
        """
        Load an existing FAISS index from disk.
        """
        if not self.index_dir.exists():
            raise FileNotFoundError(
                f"FAISS index not found at: {self.index_dir}. "
                "Build the vector store first."
            )

        return FAISS.load_local(
            folder_path=str(self.index_dir),
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True,
        )

    def get_retriever(
        self,
        vector_store: FAISS | None = None,
        k: int | None = None,
    ) -> VectorStoreRetriever:
        """
        Return a retriever from a FAISS vector store.
        """
        vector_store = vector_store or self.load_vector_store()
        k = k or self.settings.top_k_retrieval

        return vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k},
        )


if __name__ == "__main__":
    from app.document_loader import DocumentLoader
    from app.text_splitter import DocumentTextSplitter

    loader = DocumentLoader()
    documents = loader.load_documents()

    splitter = DocumentTextSplitter()
    chunks = splitter.split_documents(documents)

    manager = VectorStoreManager()
    store = manager.build_vector_store(chunks)

    retriever = manager.get_retriever(store)
    results = retriever.invoke("What is RAG?")

    print(f"Indexed chunks: {len(chunks)}")
    print(f"Retrieved documents: {len(results)}")

    for index, doc in enumerate(results, start=1):
        print("-" * 80)
        print(f"Result {index}")
        print("Metadata:", doc.metadata)
        print("Preview:")
        print(doc.page_content[:500])