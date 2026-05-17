from dataclasses import dataclass

from langchain_core.documents import Document
from openai import OpenAI

from app.config import get_settings, validate_rag_settings
from app.integrated_document_loader import IntegratedDocumentLoader
from app.integrated_text_splitter import IntegratedTextSplitter
from app.integrated_vector_store import IntegratedVectorStoreManager


@dataclass
class IntegratedRAGBuildResult:
    """
    Result returned after building the integrated RAG knowledge base.
    """

    document_count: int
    chunk_count: int


@dataclass
class IntegratedRAGResponse:
    """
    Structured response returned by the integrated RAG pipeline.
    """

    answer: str
    question: str
    sources: list[dict]
    model: str


class IntegratedRAGPipeline:
    """
    Integrated Retrieval-Augmented Generation pipeline.

    This pipeline powers the Document RAG tab inside the Multimodal AI
    Workspace.
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        validate_rag_settings(self.settings)

        self.document_loader = IntegratedDocumentLoader()
        self.text_splitter = IntegratedTextSplitter()
        self.vector_store_manager = IntegratedVectorStoreManager()
        self.client = OpenAI(api_key=self.settings.openai_api_key)

    def build_knowledge_base(self) -> IntegratedRAGBuildResult:
        """
        Load documents, split them, and build the FAISS vector index.
        """
        documents = self.document_loader.load_documents()

        if not documents:
            raise ValueError(
                "No supported PDF or TXT documents were found. "
                "Upload at least one document first."
            )

        chunks = self.text_splitter.split_documents(documents)

        if not chunks:
            raise ValueError("No text chunks were generated from the documents.")

        self.vector_store_manager.build_vector_store(
            chunks=chunks,
            save=True,
        )

        return IntegratedRAGBuildResult(
            document_count=len(documents),
            chunk_count=len(chunks),
        )

    def ask(self, question: str) -> IntegratedRAGResponse:
        """
        Answer a question using retrieved context from the vector store.
        """
        clean_question = question.strip()

        if not clean_question:
            raise ValueError("Question cannot be empty.")

        if not self.vector_store_manager.index_exists():
            raise FileNotFoundError(
                "No FAISS index found. Build the knowledge base first."
            )

        retrieved_documents = self.vector_store_manager.similarity_search(
            query=clean_question,
            top_k=self.settings.rag_top_k,
        )

        if not retrieved_documents:
            return IntegratedRAGResponse(
                answer=(
                    "I could not find relevant information in the uploaded "
                    "documents."
                ),
                question=clean_question,
                sources=[],
                model=self.settings.openai_rag_model,
            )

        context = self._format_context(retrieved_documents)

        answer = self._call_rag_model(
            question=clean_question,
            context=context,
        )

        return IntegratedRAGResponse(
            answer=answer,
            question=clean_question,
            sources=self._format_sources(retrieved_documents),
            model=self.settings.openai_rag_model,
        )

    def _call_rag_model(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Call OpenAI model with retrieved document context.
        """
        response = self.client.chat.completions.create(
            model=self.settings.openai_rag_model,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful Retrieval-Augmented Generation "
                        "assistant. Answer only using the provided context. "
                        "If the answer is not available in the context, say "
                        "that you could not find the information in the "
                        "uploaded documents. If the user asks in Arabic, "
                        "answer in Arabic. If the user asks in English, "
                        "answer in English."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Context:\n"
                        f"{context}\n\n"
                        "Question:\n"
                        f"{question}"
                    ),
                },
            ],
        )

        answer = response.choices[0].message.content

        if not answer:
            raise ValueError("RAG model returned an empty response.")

        return answer

    def _format_context(
        self,
        documents: list[Document],
    ) -> str:
        """
        Format retrieved documents as numbered context blocks.
        """
        blocks = []

        for index, document in enumerate(documents, start=1):
            metadata = document.metadata
            file_name = metadata.get("file_name", "unknown")
            page = metadata.get("page", "N/A")
            chunk_id = metadata.get("chunk_id", "N/A")

            blocks.append(
                f"[Source {index} | file={file_name} | "
                f"page={page} | chunk={chunk_id}]\n"
                f"{document.page_content}"
            )

        return "\n\n---\n\n".join(blocks)

    def _format_sources(
        self,
        documents: list[Document],
    ) -> list[dict]:
        """
        Format retrieved documents as clean source dictionaries.
        """
        sources = []

        for document in documents:
            metadata = document.metadata

            sources.append(
                {
                    "file_name": metadata.get("file_name", "unknown"),
                    "file_type": metadata.get("file_type", "unknown"),
                    "page": metadata.get("page", "N/A"),
                    "chunk_id": metadata.get("chunk_id", "N/A"),
                    "preview": document.page_content[:500],
                }
            )

        return sources