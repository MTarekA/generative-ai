from pathlib import Path

import pytest
from PIL import Image

from app.integrated_image_loader import IntegratedImageLoader


def create_test_image(path: Path) -> None:
    """
    Create a small valid image for testing.
    """
    image = Image.new("RGB", (20, 10))
    image.save(path)


def test_integrated_image_loader_loads_valid_image(
    tmp_path: Path,
) -> None:
    """
    Test that the integrated image loader loads a valid image.
    """
    image_path = tmp_path / "test_image.png"
    create_test_image(image_path)

    loader = IntegratedImageLoader()
    loaded_image = loader.load_image(image_path)

    assert loaded_image.file_name == "test_image.png"
    assert loaded_image.file_extension == ".png"
    assert loaded_image.mime_type == "image/png"
    assert loaded_image.width == 20
    assert loaded_image.height == 10
    assert loaded_image.mode == "RGB"
    assert len(loaded_image.base64_data) > 0


def test_integrated_image_loader_rejects_missing_file(
    tmp_path: Path,
) -> None:
    """
    Test that missing images raise FileNotFoundError.
    """
    image_path = tmp_path / "missing.png"

    loader = IntegratedImageLoader()

    with pytest.raises(FileNotFoundError):
        loader.load_image(image_path)


def test_integrated_image_loader_rejects_unsupported_extension(
    tmp_path: Path,
) -> None:
    """
    Test that unsupported file extensions are rejected.
    """
    file_path = tmp_path / "notes.txt"
    file_path.write_text("This is not an image.", encoding="utf-8")

    loader = IntegratedImageLoader()

    with pytest.raises(ValueError, match="Unsupported image type"):
        loader.load_image(file_path)