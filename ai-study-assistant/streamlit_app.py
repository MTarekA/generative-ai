import json
import shutil
from pathlib import Path

import streamlit as st

from app.config import RAW_DATA_DIR, VECTOR_DB_DIR
from app.document_loader import DocumentLoader
from app.rag_pipeline import RAGPipeline
from app.text_splitter import DocumentTextSplitter
from app.vector_store import VectorStoreManager


st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide",
)


def apply_custom_styles() -> None:
    """
    Apply custom CSS styles to improve the Streamlit UI.

    The styles improve spacing, chat readability, and Arabic RTL display.
    """
    st.markdown(
        """
        <style>
        .main .block-container {
            padding-top: 3rem;
            padding-bottom: 6rem;
            max-width: 1200px;
        }

        h1, h2, h3 {
            letter-spacing: -0.02em;
        }

        [data-testid="stSidebar"] {
            background-color: #f7f9fc;
        }

        [data-testid="stChatMessage"] {
            border-radius: 14px;
            padding: 0.4rem 0.6rem;
            margin-bottom: 0.8rem;
        }

        [data-testid="stChatMessage"] p {
            line-height: 1.8;
            font-size: 1rem;
        }

        .rtl-text {
            direction: rtl;
            text-align: right;
            line-height: 1.9;
            font-size: 1rem;
            unicode-bidi: plaintext;
        }

        .ltr-text {
            direction: ltr;
            text-align: left;
            line-height: 1.7;
            font-size: 1rem;
            unicode-bidi: plaintext;
        }

        .source-preview {
            direction: auto;
            text-align: start;
            line-height: 1.7;
            font-size: 0.95rem;
            background-color: #f8fafc;
            padding: 0.75rem;
            border-radius: 0.5rem;
            border: 1px solid #e5e7eb;
        }

        .small-muted {
            color: #6b7280;
            font-size: 0.9rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def is_arabic_text(text: str) -> bool:
    """
    Detect whether the given text contains Arabic characters.
    """
    return any("\u0600" <= char <= "\u06FF" for char in text)


def render_text_with_direction(text: str) -> None:
    """
    Render text with RTL support for Arabic and LTR for other languages.
    """
    css_class = "rtl-text" if is_arabic_text(text) else "ltr-text"

    st.markdown(
        f'<div class="{css_class}">{text}</div>',
        unsafe_allow_html=True,
    )


def save_uploaded_file(uploaded_file) -> Path:
    """
    Save an uploaded file into the raw data directory.
    """
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    file_path = RAW_DATA_DIR / uploaded_file.name

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path


def build_vector_index() -> tuple[int, int]:
    """
    Build the FAISS vector index from uploaded lecture documents.

    Returns:
        A tuple containing:
        - number of loaded documents
        - number of generated chunks
    """
    loader = DocumentLoader()
    documents = loader.load_documents()

    splitter = DocumentTextSplitter()
    chunks = splitter.split_documents(documents)

    manager = VectorStoreManager()
    manager.build_vector_store(chunks, save=True)

    return len(documents), len(chunks)


def list_uploaded_files() -> list[Path]:
    """
    Return all uploaded PDF and TXT files from data/raw.
    """
    if not RAW_DATA_DIR.exists():
        return []

    supported_extensions = {".pdf", ".txt"}

    return sorted(
        [
            path
            for path in RAW_DATA_DIR.iterdir()
            if path.is_file()
            and path.suffix.lower() in supported_extensions
        ]
    )


def delete_uploaded_files() -> int:
    """
    Delete all uploaded PDF and TXT files from data/raw.

    Returns:
        Number of deleted files.
    """
    deleted_count = 0
    supported_extensions = {".pdf", ".txt"}

    if not RAW_DATA_DIR.exists():
        return deleted_count

    for file_path in RAW_DATA_DIR.iterdir():
        if (
            file_path.is_file()
            and file_path.suffix.lower() in supported_extensions
        ):
            file_path.unlink()
            deleted_count += 1

    return deleted_count


def delete_faiss_index() -> bool:
    """
    Delete the local FAISS index directory if it exists.

    Returns:
        True if the index directory was deleted, otherwise False.
    """
    faiss_index_dir = VECTOR_DB_DIR / "faiss_index"

    if faiss_index_dir.exists():
        shutil.rmtree(faiss_index_dir)
        return True

    return False


def reset_application_state() -> None:
    """
    Reset Streamlit session state related to chat and knowledge base.
    """
    st.session_state.messages = []
    st.session_state.knowledge_base_ready = False


def export_chat_history() -> str:
    """
    Export the current chat history as a JSON string.
    """
    export_data = {
        "app": "AI Study Assistant",
        "messages": st.session_state.messages,
    }

    return json.dumps(
        export_data,
        ensure_ascii=False,
        indent=2,
    )


def get_pipeline() -> RAGPipeline:
    """
    Create a RAG pipeline instance.

    It is intentionally not cached at this stage to avoid stale FAISS index
    issues while developing and rebuilding the vector store.
    """
    return RAGPipeline()


def initialize_session_state() -> None:
    """
    Initialize Streamlit session state variables.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "knowledge_base_ready" not in st.session_state:
        st.session_state.knowledge_base_ready = False


def render_sources(sources: list[dict]) -> None:
    """
    Render retrieved sources in a readable format.
    """
    if not sources:
        st.warning("No sources were returned.")
        return

    for index, source in enumerate(sources, start=1):
        file_name = source.get("file_name", "unknown")
        file_type = source.get("file_type", "unknown")
        page = source.get("page", "N/A")
        chunk_id = source.get("chunk_id", "N/A")
        preview = source.get("preview", "")

        with st.expander(f"Source {index}: {file_name}"):
            st.write(f"File type: {file_type}")
            st.write(f"Page: {page}")
            st.write(f"Chunk ID: {chunk_id}")
            st.write("Preview:")
            st.markdown(
                f'<div class="source-preview">{preview}</div>',
                unsafe_allow_html=True,
            )


def render_chat_history() -> None:
    """
    Render previous user questions and assistant answers.
    """
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]

        with st.chat_message(role):
            render_text_with_direction(content)

            if role == "assistant" and message.get("sources"):
                st.write("Sources:")
                render_sources(message["sources"])


def render_sidebar() -> None:
    """
    Render sidebar controls for document upload, knowledge base building,
    chat export, and reset options.
    """
    with st.sidebar:
        st.header("Document Setup")

        uploaded_files = st.file_uploader(
            "Upload PDF or TXT lecture files",
            type=["pdf", "txt"],
            accept_multiple_files=True,
        )

        if uploaded_files:
            for uploaded_file in uploaded_files:
                saved_path = save_uploaded_file(uploaded_file)
                st.success(f"Saved: {saved_path.name}")

        st.divider()

        existing_files = list_uploaded_files()

        st.subheader("Available Documents")

        if existing_files:
            for file_path in existing_files:
                st.write(f"- {file_path.name}")
        else:
            st.info("No PDF or TXT files found in data/raw.")

        st.divider()

        if st.button("Build / Rebuild Knowledge Base"):
            try:
                with st.spinner("Building vector index..."):
                    document_count, chunk_count = build_vector_index()

                st.session_state.knowledge_base_ready = True

                st.success(
                    "Knowledge base built successfully. "
                    f"Documents: {document_count}, Chunks: {chunk_count}"
                )

            except Exception as error:
                st.session_state.knowledge_base_ready = False
                st.error(f"Failed to build knowledge base: {error}")

        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.success("Chat history cleared.")

        if st.session_state.messages:
            chat_json = export_chat_history()

            st.download_button(
                label="Download Chat History",
                data=chat_json,
                file_name="chat_history.json",
                mime="application/json",
            )

        st.divider()

        st.subheader("Reset Options")

        if st.button("Delete Uploaded Files"):
            deleted_count = delete_uploaded_files()
            st.session_state.knowledge_base_ready = False

            st.success(f"Deleted uploaded files: {deleted_count}")

        if st.button("Delete FAISS Index"):
            deleted = delete_faiss_index()
            st.session_state.knowledge_base_ready = False

            if deleted:
                st.success("FAISS index deleted successfully.")
            else:
                st.info("No FAISS index found.")

        if st.button("Full Reset"):
            deleted_count = delete_uploaded_files()
            index_deleted = delete_faiss_index()
            reset_application_state()

            st.success(
                "Application reset completed. "
                f"Deleted files: {deleted_count}. "
                f"Index deleted: {index_deleted}."
            )


def handle_user_question(question: str) -> None:
    """
    Process a user question through the RAG pipeline.
    """
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        render_text_with_direction(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                pipeline = get_pipeline()
                response = pipeline.ask(question)

            render_text_with_direction(response.answer)

            st.write("Sources:")
            render_sources(response.sources)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response.answer,
                    "sources": response.sources,
                }
            )

        except Exception as error:
            error_message = f"Failed to answer question: {error}"
            st.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                    "sources": [],
                }
            )


def render_about_section() -> None:
    """
    Render project information, architecture, and usage instructions.
    """
    st.subheader("About this project")

    st.write(
        """
        AI Study Assistant is a Retrieval-Augmented Generation application
        designed to help students study lecture documents more effectively.
        Users can upload PDF or TXT files, build a local FAISS knowledge base,
        and ask questions grounded in the uploaded materials.
        """
    )

    st.subheader("What the system does")

    st.markdown(
        """
        - Loads lecture documents from uploaded files
        - Splits long documents into smaller chunks
        - Generates embeddings for semantic search
        - Stores document vectors locally using FAISS
        - Retrieves relevant chunks for each question
        - Uses an LLM to generate an answer based on retrieved context
        - Shows the sources used for each answer
        - Supports Arabic and English questions
        """
    )

    st.subheader("System architecture")

    st.code(
        """
User uploads PDF / TXT
        ↓
Document Loader
        ↓
Text Splitter
        ↓
Embedding Model
        ↓
FAISS Vector Store
        ↓
Retriever
        ↓
Prompt + LLM
        ↓
Answer + Sources
        """,
        language="text",
    )

    st.subheader("How to use it")

    st.markdown(
        """
        1. Upload one or more PDF/TXT lecture files from the sidebar.
        2. Click `Build / Rebuild Knowledge Base`.
        3. Ask a question in the chat input.
        4. Review the answer and the retrieved sources.
        5. Download the chat history if needed.
        """
    )

    st.subheader("Quality and safety behavior")

    st.markdown(
        """
        - The assistant answers using the retrieved document context.
        - If the answer is not present in the uploaded documents, the assistant
          should clearly say that it could not find the information.
        - The system displays retrieved sources to make answers easier to verify.
        - A separate evaluation script is included to check basic RAG behavior.
        """
    )

    st.subheader("Limitations")

    st.markdown(
        """
        - The answer quality depends on the uploaded documents.
        - Very large documents may require more processing time.
        - The current version uses local FAISS storage and is designed for a
          single-user demo.
        - The project is educational and not intended as a production deployment.
        """
    )


def main() -> None:
    """
    Main Streamlit application.
    """
    initialize_session_state()
    apply_custom_styles()

    st.title("AI Study Assistant")
    st.caption(
        "Upload lecture files, build a FAISS knowledge base, "
        "and ask grounded questions using Retrieval-Augmented Generation."
    )

    render_sidebar()

    chat_tab, about_tab = st.tabs(["Chat", "About Project"])

    with chat_tab:
        st.subheader("Chat with your lecture documents")

        if not list_uploaded_files():
            st.info(
                "Start by uploading at least one PDF or TXT file "
                "from the sidebar."
            )

        render_chat_history()

        question = st.chat_input(
            "Ask a question about your uploaded lecture documents..."
        )

        if question:
            handle_user_question(question)

    with about_tab:
        render_about_section()


if __name__ == "__main__":
    main()