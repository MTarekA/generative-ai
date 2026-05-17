from dataclasses import dataclass
from pathlib import Path

from openai import OpenAI

from app.config import get_settings, validate_openai_settings
from app.integrated_audio_loader import (
    IntegratedAudioLoader,
    IntegratedLoadedAudio,
)


@dataclass
class IntegratedTranscriptionResponse:
    """
    Structured response returned by the integrated transcription pipeline.
    """

    transcript: str
    audio_metadata: dict
    model: str


class IntegratedTranscriptionPipeline:
    """
    Integrated speech-to-text pipeline for the Multimodal AI Workspace.
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        validate_openai_settings(self.settings)

        self.audio_loader = IntegratedAudioLoader()
        self.client = OpenAI(api_key=self.settings.openai_api_key)

    def transcribe_audio(
        self,
        audio_path: str | Path,
    ) -> IntegratedTranscriptionResponse:
        """
        Transcribe an audio file using OpenAI transcription model.
        """
        loaded_audio = self.audio_loader.load_audio(audio_path)

        transcript = self._call_transcription_model(loaded_audio)

        if not transcript.strip():
            raise ValueError("Transcription model returned an empty transcript.")

        return IntegratedTranscriptionResponse(
            transcript=transcript,
            audio_metadata=self._extract_audio_metadata(loaded_audio),
            model=self.settings.openai_transcription_model,
        )

    def _call_transcription_model(
        self,
        loaded_audio: IntegratedLoadedAudio,
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
            raise ValueError("OpenAI transcription response did not contain text.")

        return transcript

    def _extract_audio_metadata(
        self,
        loaded_audio: IntegratedLoadedAudio,
    ) -> dict:
        """
        Extract clean audio metadata.
        """
        return {
            "file_name": loaded_audio.file_name,
            "file_extension": loaded_audio.file_extension,
            "file_size_bytes": loaded_audio.file_size_bytes,
            "file_size_mb": loaded_audio.file_size_mb,
        }