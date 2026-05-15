from pathlib import Path

import pytest

from app.audio_loader import AudioLoader


def create_dummy_audio_file(path: Path) -> None:
    """
    Create a small dummy audio file for loader tests.

    The file does not need to contain real audio because AudioLoader
    only validates path, extension, and file metadata.
    """
    path.write_bytes(b"dummy audio content")


def test_audio_loader_loads_supported_audio_file(tmp_path: Path) -> None:
    """
    Test that AudioLoader can load a supported audio file.
    """
    audio_path = tmp_path / "test_audio.mp3"
    create_dummy_audio_file(audio_path)

    loader = AudioLoader()
    loaded_audio = loader.load_audio(audio_path)

    assert loaded_audio.file_name == "test_audio.mp3"
    assert loaded_audio.file_extension == ".mp3"
    assert loaded_audio.file_size_bytes > 0
    assert loaded_audio.file_size_mb >= 0


def test_audio_loader_rejects_unsupported_file(tmp_path: Path) -> None:
    """
    Test that AudioLoader rejects unsupported file extensions.
    """
    file_path = tmp_path / "notes.txt"
    file_path.write_text("This is not an audio file.", encoding="utf-8")

    loader = AudioLoader()

    with pytest.raises(ValueError, match="Unsupported audio type"):
        loader.load_audio(file_path)


def test_audio_loader_rejects_missing_file(tmp_path: Path) -> None:
    """
    Test that AudioLoader raises FileNotFoundError for missing files.
    """
    missing_path = tmp_path / "missing.mp3"

    loader = AudioLoader()

    with pytest.raises(FileNotFoundError):
        loader.load_audio(missing_path)