from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from app.config import (
    INTEGRATED_VECTOR_DIR,
    get_settings,
    validate_openai_settings,
)


class IntegratedVectorStoreManager:
    """
    Build, save, load, and query a FAISS vector store for integrated RAG.
    """

    def __init__(
        self,
        vector_dir: Path | None = None,
    ) -> None:
        self.settings = get_settings()
        validate_openai_settings(self.settings)

        self.vector_dir = vector_dir or INTEGRATED_VECTOR_DIR
        self.index_dir = self.vector_dir / "faiss_index"

        self.embeddings = OpenAIEmbeddings(
            model=self.settings.openai_embedding_model,
            api_key=self.settings.openai_api_key,
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
            raise ValueError("Cannot build vector store from empty chunks.")

        vector_store = FAISS.from_documents(
            documents=chunks,
            embedding=self.embeddings,
        )

        if save:
            self.save_vector_store(vector_store)

        return vector_store

    def save_vector_store(self, vector_store: FAISS) -> None:
        """
        Save FAISS vector store locally.
        """
        self.index_dir.mkdir(parents=True, exist_ok=True)
        vector_store.save_local(str(self.index_dir))

    def load_vector_store(self) -> FAISS:
        """
        Load a saved FAISS vector store.
        """
        if not self.index_dir.exists():
            raise FileNotFoundError(
                f"FAISS index not found: {self.index_dir}"
            )

        return FAISS.load_local(
            folder_path=str(self.index_dir),
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True,
        )

    def similarity_search(
        self,
        query: str,
        top_k: int | None = None,
    ) -> list[Document]:
        """
        Search the vector store for relevant chunks.
        """
        clean_query = query.strip()

        if not clean_query:
            raise ValueError("Query cannot be empty.")

        vector_store = self.load_vector_store()

        return vector_store.similarity_search(
            query=clean_query,
            k=top_k or self.settings.rag_top_k,
        )

    def index_exists(self) -> bool:
        """
        Return whether a local FAISS index exists.
        """
        return (
            self.index_dir.exists()
            and (self.index_dir / "index.faiss").exists()
            and (self.index_dir / "index.pkl").exists()
        )