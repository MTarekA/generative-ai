from dataclasses import dataclass
from pathlib import Path


SUPPORTED_AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".webm",
    ".mp4",
}


@dataclass
class IntegratedLoadedAudio:
    """
    Structured representation of a loaded audio file.
    """

    file_path: Path
    file_name: str
    file_extension: str
    file_size_bytes: int
    file_size_mb: float


class IntegratedAudioLoader:
    """
    Load and validate audio files for the integrated audio demo.
    """

    def __init__(
        self,
        supported_extensions: set[str] | None = None,
    ) -> None:
        self.supported_extensions = (
            supported_extensions or SUPPORTED_AUDIO_EXTENSIONS
        )

    def load_audio(self, audio_path: str | Path) -> IntegratedLoadedAudio:
        """
        Load an audio file and extract basic metadata.
        """
        path = Path(audio_path)

        self._validate_audio_path(path)

        file_size_bytes = path.stat().st_size
        file_size_mb = round(file_size_bytes / (1024 * 1024), 2)

        return IntegratedLoadedAudio(
            file_path=path,
            file_name=path.name,
            file_extension=path.suffix.lower(),
            file_size_bytes=file_size_bytes,
            file_size_mb=file_size_mb,
        )

    def _validate_audio_path(self, audio_path: Path) -> None:
        """
        Validate that the audio path exists and has a supported extension.
        """
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        if not audio_path.is_file():
            raise ValueError(f"Path is not a file: {audio_path}")

        extension = audio_path.suffix.lower()

        if extension not in self.supported_extensions:
            raise ValueError(
                f"Unsupported audio type: {extension}. "
                f"Supported types: {self.supported_extensions}"
            )