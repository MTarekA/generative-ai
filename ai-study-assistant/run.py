import argparse

from app.document_loader import DocumentLoader
from app.logger import get_logger
from app.rag_pipeline import RAGPipeline
from app.text_splitter import DocumentTextSplitter
from app.vector_store import VectorStoreManager


logger = get_logger(__name__)


def build_index() -> None:
    """
    Build the FAISS vector index from documents in data/raw.
    """
    logger.info("Loading documents...")
    loader = DocumentLoader()
    documents = loader.load_documents()
    logger.info("Loaded documents: %s", len(documents))

    logger.info("Splitting documents into chunks...")
    splitter = DocumentTextSplitter()
    chunks = splitter.split_documents(documents)
    logger.info("Generated chunks: %s", len(chunks))

    logger.info("Building FAISS vector store...")
    manager = VectorStoreManager()
    manager.build_vector_store(chunks, save=True)

    logger.info("Vector store built and saved successfully.")


def ask_question() -> None:
    """
    Start a simple terminal-based question-answering loop.
    """
    logger.info("Starting AI Study Assistant...")

    print("AI Study Assistant is ready.")
    print("Type your question and press Enter.")
    print("Type 'exit' or 'quit' to stop.")
    print("-" * 80)

    pipeline = RAGPipeline()

    while True:
        question = input("\nYour question: ").strip()

        if question.lower() in {"exit", "quit"}:
            logger.info("User ended the session.")
            print("Goodbye.")
            break

        if not question:
            print("Please enter a valid question.")
            continue

        try:
            logger.info("Received question: %s", question)
            response = pipeline.ask(question)
            logger.info("Answer generated successfully.")
        except Exception as error:
            logger.exception("Error while answering question.")
            print(f"Error while answering: {error}")
            continue

        print("\nAnswer:")
        print(response.answer)

        print("\nSources:")
        for index, source in enumerate(response.sources, start=1):
            file_name = source.get("file_name", "unknown")
            file_type = source.get("file_type", "unknown")
            page = source.get("page", "N/A")
            chunk_id = source.get("chunk_id", "N/A")
            preview = source.get("preview", "")

            print("-" * 80)
            print(f"Source {index}")
            print(f"File: {file_name}")
            print(f"Type: {file_type}")
            print(f"Page: {page}")
            print(f"Chunk: {chunk_id}")
            print(f"Preview: {preview}")


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="AI Study Assistant command-line interface"
    )

    parser.add_argument(
        "command",
        choices=["build", "ask"],
        help="Command to run: build the index or ask questions",
    )

    return parser.parse_args()


def main() -> None:
    """
    Main entry point for the application.
    """
    args = parse_args()

    if args.command == "build":
        build_index()
        return

    if args.command == "ask":
        ask_question()
        return

    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    main()