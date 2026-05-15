import argparse
from pathlib import Path

from app.config import ensure_directories
from app.logger import get_logger
from app.result_manager import ResultManager
from app.summarization_pipeline import SummarizationPipeline
from app.transcription_pipeline import TranscriptionPipeline


logger = get_logger(__name__)


def analyze_audio(audio_path: str) -> None:
    """
    Transcribe and summarize an audio file from the command line.
    """
    path = Path(audio_path)

    logger.info("Starting audio analysis.")
    logger.info("Audio path: %s", path)

    print("=" * 80)
    print("AI Voice Meeting Assistant")
    print("=" * 80)

    try:
        print("\nStep 1: Transcribing audio...")
        logger.info("Starting transcription.")

        transcription_pipeline = TranscriptionPipeline()
        transcription_response = transcription_pipeline.transcribe_audio(path)

        logger.info("Transcription completed successfully.")
        print("Transcription completed.")

        print("\nStep 2: Summarizing transcript...")
        logger.info("Starting summarization.")

        summarization_pipeline = SummarizationPipeline()
        summary_response = summarization_pipeline.summarize_transcript(
            transcription_response.transcript
        )

        logger.info("Summarization completed successfully.")
        print("Summarization completed.")

        print("\nStep 3: Saving result...")
        logger.info("Saving analysis result.")

        result_manager = ResultManager()
        saved_result_path = result_manager.save_audio_analysis_result(
            audio_path=path,
            transcript=transcription_response.transcript,
            summary=summary_response.summary,
            audio_metadata=transcription_response.audio_metadata,
            transcription_model=transcription_response.model,
            summary_model=summary_response.model,
        )

        logger.info("Result saved to: %s", saved_result_path)
        print("Result saved successfully.")

    except Exception:
        logger.exception("Audio analysis failed.")
        raise

    print("\nAudio metadata:")
    for key, value in transcription_response.audio_metadata.items():
        print(f"- {key}: {value}")

    print("\nTranscript:")
    print(transcription_response.transcript)

    print("\nSummary:")
    print(summary_response.summary)

    print("\nSaved result:")
    print(saved_result_path)


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="AI Voice Meeting Assistant CLI"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Transcribe and summarize an audio file",
    )

    analyze_parser.add_argument(
        "audio_path",
        help="Path to the audio file",
    )

    return parser.parse_args()


def main() -> None:
    """
    Main entry point for the CLI.
    """
    ensure_directories()
    args = parse_args()

    if args.command == "analyze":
        analyze_audio(args.audio_path)
        return

    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    main()