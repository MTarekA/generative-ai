from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
UPLOADED_IMAGES_DIR = DATA_DIR / "uploaded_images"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
LOGS_DIR = PROJECT_ROOT / "logs"


class Settings(BaseSettings):
    """
    Central settings for the AI Image Understanding Assistant.
    """

    app_name: str = Field(
        default="AI Image Understanding Assistant",
        alias="APP_NAME",
    )
    debug: bool = Field(default=True, alias="DEBUG")

    openai_api_key: str | None = Field(
        default=None,
        alias="OPENAI_API_KEY",
    )
    google_api_key: str | None = Field(
        default=None,
        alias="GOOGLE_API_KEY",
    )

    vision_provider: Literal["openai", "gemini"] = Field(
        default="openai",
        alias="VISION_PROVIDER",
    )

    openai_vision_model: str = Field(
        default="gpt-4o-mini",
        alias="OPENAI_VISION_MODEL",
    )
    gemini_vision_model: str = Field(
        default="gemini-1.5-flash",
        alias="GEMINI_VISION_MODEL",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


def get_settings() -> Settings:
    """
    Return project settings.
    """
    return Settings()


def validate_settings(settings: Settings | None = None) -> None:
    """
    Validate required settings before running the application.
    """
    settings = settings or get_settings()

    if settings.vision_provider == "openai" and not settings.openai_api_key:
        raise ValueError(
            "OPENAI_API_KEY is required when VISION_PROVIDER=openai"
        )

    if settings.vision_provider == "gemini" and not settings.google_api_key:
        raise ValueError(
            "GOOGLE_API_KEY is required when VISION_PROVIDER=gemini"
        )


def ensure_directories() -> None:
    """
    Create required project directories if they do not exist.
    """
    UPLOADED_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    settings = get_settings()
    ensure_directories()

    print("Project root:", PROJECT_ROOT)
    print("Uploaded images dir:", UPLOADED_IMAGES_DIR)
    print("Outputs dir:", OUTPUTS_DIR)
    print("Logs dir:", LOGS_DIR)
    print("App name:", settings.app_name)
    print("Vision provider:", settings.vision_provider)
    print("OpenAI vision model:", settings.openai_vision_model)
    print("Gemini vision model:", settings.gemini_vision_model)