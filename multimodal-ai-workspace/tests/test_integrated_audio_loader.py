from pathlib import Path

import pytest

from app.integrated_audio_loader import IntegratedAudioLoader


def create_test_audio_file(path: Path) -> None:
    """
    Create a small dummy audio-like file for loader metadata tests.

    The loader validates file existence, extension, and size only.
    It does not decode audio content.
    """
    path.write_bytes(b"fake audio content for testing")


def test_integrated_audio_loader_loads_valid_audio(
    tmp_path: Path,
) -> None:
    """
    Test that the integrated audio loader loads a supported audio file.
    """
    audio_path = tmp_path / "test_audio.mp3"
    create_test_audio_file(audio_path)

    loader = IntegratedAudioLoader()
    loaded_audio = loader.load_audio(audio_path)

    assert loaded_audio.file_name == "test_audio.mp3"
    assert loaded_audio.file_extension == ".mp3"
    assert loaded_audio.file_size_bytes > 0
    assert loaded_audio.file_size_mb >= 0


def test_integrated_audio_loader_rejects_missing_file(
    tmp_path: Path,
) -> None:
    """
    Test that missing audio files raise FileNotFoundError.
    """
    audio_path = tmp_path / "missing_audio.mp3"

    loader = IntegratedAudioLoader()

    with pytest.raises(FileNotFoundError):
        loader.load_audio(audio_path)


def test_integrated_audio_loader_rejects_unsupported_extension(
    tmp_path: Path,
) -> None:
    """
    Test that unsupported file extensions are rejected.
    """
    file_path = tmp_path / "notes.txt"
    file_path.write_text("This is not an audio file.", encoding="utf-8")

    loader = IntegratedAudioLoader()

    with pytest.raises(ValueError, match="Unsupported audio type"):
        loader.load_audio(file_path)