import argparse
from pathlib import Path

from app.config import ensure_directories
from app.logger import get_logger
from app.vision_pipeline import VisionPipeline


logger = get_logger(__name__)


def analyze_image(image_path: str, question: str | None = None) -> None:
    """
    Analyze an image from the command line.
    """
    path = Path(image_path)

    logger.info("Starting image analysis.")
    logger.info("Image path: %s", path)

    pipeline = VisionPipeline()
    response = pipeline.analyze_image(
        image_path=path,
        question=question,
    )

    logger.info("Image analysis completed successfully.")

    print("=" * 80)
    print("AI Image Understanding Assistant")
    print("=" * 80)

    print("\nImage metadata:")
    for key, value in response.image_metadata.items():
        print(f"- {key}: {value}")

    print("\nQuestion:")
    print(response.question)

    print("\nAnswer:")
    print(response.answer)


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="AI Image Understanding Assistant CLI"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze an image using a vision model",
    )

    analyze_parser.add_argument(
        "image_path",
        help="Path to the image file",
    )

    analyze_parser.add_argument(
        "--question",
        "-q",
        default=None,
        help="Optional question about the image",
    )

    return parser.parse_args()


def main() -> None:
    """
    Main entry point for the CLI.
    """
    ensure_directories()
    args = parse_args()

    if args.command == "analyze":
        analyze_image(
            image_path=args.image_path,
            question=args.question,
        )
        return

    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    main()