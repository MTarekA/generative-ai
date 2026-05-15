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
class LoadedAudio:
    """
    Structured representation of a loaded audio file.

    file_path:
        Path to the audio file.

    file_name:
        Audio file name.

    file_extension:
        Audio extension such as .mp3 or .wav.

    file_size_bytes:
        File size in bytes.

    file_size_mb:
        File size in megabytes.
    """

    file_path: Path
    file_name: str
    file_extension: str
    file_size_bytes: int
    file_size_mb: float


class AudioLoader:
    """
    Load and validate audio files for transcription.
    """

    def __init__(
        self,
        supported_extensions: set[str] | None = None,
    ) -> None:
        self.supported_extensions = (
            supported_extensions or SUPPORTED_AUDIO_EXTENSIONS
        )

    def load_audio(self, audio_path: str | Path) -> LoadedAudio:
        """
        Load an audio file from disk and return structured metadata.
        """
        path = Path(audio_path)

        self._validate_audio_path(path)

        file_size_bytes = path.stat().st_size
        file_size_mb = round(file_size_bytes / (1024 * 1024), 2)

        return LoadedAudio(
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


if __name__ == "__main__":
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
        print(f"Supported types: {SUPPORTED_AUDIO_EXTENSIONS}")
    else:
        loader = AudioLoader()
        loaded_audio = loader.load_audio(audio_files[0])

        print("Audio loaded successfully.")
        print("File name:", loaded_audio.file_name)
        print("Extension:", loaded_audio.file_extension)
        print("Size bytes:", loaded_audio.file_size_bytes)
        print("Size MB:", loaded_audio.file_size_mb)