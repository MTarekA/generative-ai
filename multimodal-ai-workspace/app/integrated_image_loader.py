import base64
import mimetypes
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


SUPPORTED_IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
}


@dataclass
class IntegratedLoadedImage:
    """
    Structured representation of a loaded image.
    """

    file_path: Path
    file_name: str
    file_extension: str
    mime_type: str
    width: int
    height: int
    mode: str
    base64_data: str


class IntegratedImageLoader:
    """
    Load, validate, and encode images for the integrated vision demo.
    """

    def __init__(
        self,
        supported_extensions: set[str] | None = None,
    ) -> None:
        self.supported_extensions = (
            supported_extensions or SUPPORTED_IMAGE_EXTENSIONS
        )

    def load_image(self, image_path: str | Path) -> IntegratedLoadedImage:
        """
        Load an image, extract metadata, and encode it as Base64.
        """
        path = Path(image_path)

        self._validate_image_path(path)

        with Image.open(path) as image:
            width, height = image.size
            mode = image.mode

        mime_type = self._get_mime_type(path)
        base64_data = self._encode_image_to_base64(path)

        return IntegratedLoadedImage(
            file_path=path,
            file_name=path.name,
            file_extension=path.suffix.lower(),
            mime_type=mime_type,
            width=width,
            height=height,
            mode=mode,
            base64_data=base64_data,
        )

    def _validate_image_path(self, image_path: Path) -> None:
        """
        Validate that the image exists and has a supported extension.
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

    def _get_mime_type(self, image_path: Path) -> str:
        """
        Return image MIME type.
        """
        mime_type, _ = mimetypes.guess_type(image_path)

        if not mime_type:
            raise ValueError(f"Could not determine MIME type: {image_path}")

        return mime_type

    def _encode_image_to_base64(self, image_path: Path) -> str:
        """
        Encode image file as a Base64 string.
        """
        with open(image_path, "rb") as file:
            return base64.b64encode(file.read()).decode("utf-8")