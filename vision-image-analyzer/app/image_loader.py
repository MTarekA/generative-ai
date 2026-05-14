import base64
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


@dataclass
class LoadedImage:
    """
    Structured representation of a loaded image.

    file_path:
        Path to the image file.

    file_name:
        Image file name.

    file_extension:
        Image extension such as .png or .jpg.

    width:
        Image width in pixels.

    height:
        Image height in pixels.

    mode:
        Image color mode, for example RGB or RGBA.

    base64_data:
        Base64-encoded image content.

    mime_type:
        MIME type required for API calls.
    """

    file_path: Path
    file_name: str
    file_extension: str
    width: int
    height: int
    mode: str
    base64_data: str
    mime_type: str


class ImageLoader:
    """
    Load and validate image files for vision model processing.
    """

    def __init__(
        self,
        supported_extensions: set[str] | None = None,
    ) -> None:
        self.supported_extensions = (
            supported_extensions or SUPPORTED_IMAGE_EXTENSIONS
        )

    def load_image(self, image_path: str | Path) -> LoadedImage:
        """
        Load an image from disk and return structured image data.
        """
        path = Path(image_path)

        self._validate_image_path(path)

        with Image.open(path) as image:
            width, height = image.size
            mode = image.mode

        base64_data = self._encode_image_to_base64(path)
        mime_type = self._get_mime_type(path)

        return LoadedImage(
            file_path=path,
            file_name=path.name,
            file_extension=path.suffix.lower(),
            width=width,
            height=height,
            mode=mode,
            base64_data=base64_data,
            mime_type=mime_type,
        )

    def _validate_image_path(self, image_path: Path) -> None:
        """
        Validate that the image path exists and has a supported extension.
        """
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")

        if not image_path.is_file():
            raise ValueError(f"Path is not a file: {image_path}")

        extension = image_path.suffix.lower()

        if extension not in self.supported_extensions:
            raise ValueError(
                f"Unsupported image type: {extension}. "
                f"Supported types: {self.supported_extensions}"
            )

    def _encode_image_to_base64(self, image_path: Path) -> str:
        """
        Encode image content as a Base64 string.
        """
        with open(image_path, "rb") as image_file:
            encoded_bytes = base64.b64encode(image_file.read())

        return encoded_bytes.decode("utf-8")

    def _get_mime_type(self, image_path: Path) -> str:
        """
        Return the MIME type for a supported image file.
        """
        extension = image_path.suffix.lower()

        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
        }

        return mime_types[extension]


if __name__ == "__main__":
    from app.config import UPLOADED_IMAGES_DIR, ensure_directories

    ensure_directories()

    image_files = [
        path
        for path in UPLOADED_IMAGES_DIR.iterdir()
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
    ]

    if not image_files:
        print(f"No supported images found in: {UPLOADED_IMAGES_DIR}")
        print(f"Supported types: {SUPPORTED_IMAGE_EXTENSIONS}")
    else:
        loader = ImageLoader()
        loaded_image = loader.load_image(image_files[0])

        print("Image loaded successfully.")
        print("File name:", loaded_image.file_name)
        print("Extension:", loaded_image.file_extension)
        print("Size:", loaded_image.width, "x", loaded_image.height)
        print("Mode:", loaded_image.mode)
        print("MIME type:", loaded_image.mime_type)
        print("Base64 preview:", loaded_image.base64_data[:80])