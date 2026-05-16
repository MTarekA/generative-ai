import argparse

from app.assistant_pipeline import AssistantPipeline
from app.config import ensure_directories
from app.logger import get_logger


logger = get_logger(__name__)


def ask_once(message: str) -> None:
    """
    Send a single message to the assistant and print the response.
    """
    logger.info("Running single assistant command.")
    logger.info("User message: %s", message)

    assistant = AssistantPipeline()

    try:
        response = assistant.handle_message(message)
    except Exception:
        logger.exception("Assistant command failed.")
        raise

    logger.info("Tool used: %s", response.tool_name)

    print("=" * 80)
    print("MCP Workspace Assistant")
    print("=" * 80)
    print(f"Tool used: {response.tool_name}")
    print("-" * 80)
    print(response.message)


def interactive_chat() -> None:
    """
    Start an interactive terminal chat session.
    """
    logger.info("Starting interactive chat session.")

    assistant = AssistantPipeline()

    print("=" * 80)
    print("MCP Workspace Assistant")
    print("=" * 80)
    print("Type 'help' to see supported commands.")
    print("Type 'exit' or 'quit' to stop.")
    print("=" * 80)

    while True:
        user_message = input("\nYou: ").strip()

        if user_message.lower() in {"exit", "quit"}:
            logger.info("Interactive chat session ended by user.")
            print("Goodbye.")
            break

        if not user_message:
            continue

        logger.info("User message: %s", user_message)

        try:
            response = assistant.handle_message(user_message)

            logger.info("Tool used: %s", response.tool_name)

            print(f"\nTool used: {response.tool_name}")
            print("Assistant:")
            print(response.message)

        except Exception as error:
            logger.exception("Assistant command failed.")
            print(f"Error: {error}")


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="MCP Workspace Assistant CLI"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    ask_parser = subparsers.add_parser(
        "ask",
        help="Send one command to the assistant",
    )

    ask_parser.add_argument(
        "message",
        help="Command/message for the assistant",
    )

    subparsers.add_parser(
        "chat",
        help="Start interactive assistant chat",
    )

    return parser.parse_args()


def main() -> None:
    """
    Main CLI entry point.
    """
    ensure_directories()
    args = parse_args()

    logger.info("CLI command: %s", args.command)

    if args.command == "ask":
        ask_once(args.message)
        return

    if args.command == "chat":
        interactive_chat()
        return

    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    main()