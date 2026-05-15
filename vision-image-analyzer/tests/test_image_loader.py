from pathlib import Path

import pytest
from PIL import Image

from app.image_loader import ImageLoader


def create_test_image(path: Path) -> None:
    """
    Create a small test image for local testing.
    """
    image = Image.new("RGB", (100, 50))
    image.save(path)


def test_image_loader_loads_png_image(tmp_path: Path) -> None:
    """
    Test that ImageLoader can load a valid PNG image.
    """
    image_path = tmp_path / "test_image.png"
    create_test_image(image_path)

    loader = ImageLoader()
    loaded_image = loader.load_image(image_path)

    assert loaded_image.file_name == "test_image.png"
    assert loaded_image.file_extension == ".png"
    assert loaded_image.width == 100
    assert loaded_image.height == 50
    assert loaded_image.mode == "RGB"
    assert loaded_image.mime_type == "image/png"
    assert len(loaded_image.base64_data) > 0


def test_image_loader_rejects_unsupported_file(tmp_path: Path) -> None:
    """
    Test that ImageLoader rejects unsupported file extensions.
    """
    file_path = tmp_path / "notes.txt"
    file_path.write_text("This is not an image.", encoding="utf-8")

    loader = ImageLoader()

    with pytest.raises(ValueError, match="Unsupported image type"):
        loader.load_image(file_path)


def test_image_loader_rejects_missing_file(tmp_path: Path) -> None:
    """
    Test that ImageLoader raises FileNotFoundError for missing files.
    """
    missing_path = tmp_path / "missing.png"

    loader = ImageLoader()

    with pytest.raises(FileNotFoundError):
        loader.load_image(missing_path)