from dataclasses import dataclass
from pathlib import Path

from openai import OpenAI

from app.audio_loader import AudioLoader, LoadedAudio
from app.config import get_settings, validate_settings


@dataclass
class TranscriptionResponse:
    """
    Structured response returned by the transcription pipeline.

    transcript:
        The transcribed text returned by the speech-to-text model.

    audio_metadata:
        Basic metadata about the processed audio file.

    model:
        The transcription model used.
    """

    transcript: str
    audio_metadata: dict
    model: str


class TranscriptionPipeline:
    """
    End-to-end audio transcription pipeline.

    Responsibilities:
    - Load and validate the audio file
    - Send the audio file to the transcription model
    - Return transcript and audio metadata
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        validate_settings(self.settings)

        if self.settings.transcription_provider != "openai":
            raise ValueError(
                "This pipeline currently supports only "
                "TRANSCRIPTION_PROVIDER=openai."
            )

        self.audio_loader = AudioLoader()
        self.client = OpenAI(api_key=self.settings.openai_api_key)

    def transcribe_audio(
        self,
        audio_path: str | Path,
    ) -> TranscriptionResponse:
        """
        Transcribe an audio file using OpenAI transcription.
        """
        loaded_audio = self.audio_loader.load_audio(audio_path)

        transcript = self._call_openai_transcription(loaded_audio)

        return TranscriptionResponse(
            transcript=transcript,
            audio_metadata=self._extract_audio_metadata(loaded_audio),
            model=self.settings.openai_transcription_model,
        )

    def _call_openai_transcription(
        self,
        loaded_audio: LoadedAudio,
    ) -> str:
        """
        Call OpenAI transcription model.
        """
        with open(loaded_audio.file_path, "rb") as audio_file:
            response = self.client.audio.transcriptions.create(
                model=self.settings.openai_transcription_model,
                file=audio_file,
            )

        transcript = response.text

        if not transcript:
            raise ValueError("Transcription model returned an empty response.")

        return transcript

    def _extract_audio_metadata(
        self,
        loaded_audio: LoadedAudio,
    ) -> dict:
        """
        Extract clean audio metadata for the response.
        """
        return {
            "file_name": loaded_audio.file_name,
            "file_extension": loaded_audio.file_extension,
            "file_size_bytes": loaded_audio.file_size_bytes,
            "file_size_mb": loaded_audio.file_size_mb,
        }


if __name__ == "__main__":
    from app.audio_loader import SUPPORTED_AUDIO_EXTENSIONS
    from app.config import UPLOADED_AUDIO_DIR, ensure_directories

    ensure_directories()

    audio_files = [
        path
        for path in UPLOADED_AUDIO_DIR.iterdir()
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS
    ]

    if not audio_files:
        print(f"No supported audio files found in: {UPLOADED_AUDIO_DIR}")
        print("Add a test audio file first, then run this file again.")
    else:
        pipeline = TranscriptionPipeline()
        response = pipeline.transcribe_audio(audio_files[0])

        print("Transcript:")
        print(response.transcript)

        print("\nAudio metadata:")
        print(response.audio_metadata)

        print("\nModel:")
        print(response.model)