from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PORTFOLIO_ROOT = PROJECT_ROOT.parent

ASSETS_DIR = PROJECT_ROOT / "assets"
SCREENSHOTS_DIR = ASSETS_DIR / "screenshots"
DIAGRAMS_DIR = ASSETS_DIR / "diagrams"
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
LOGS_DIR = PROJECT_ROOT / "logs"

INTEGRATED_UPLOADS_DIR = PROJECT_ROOT / "integrated_uploads"
INTEGRATED_IMAGES_DIR = INTEGRATED_UPLOADS_DIR / "images"


class Settings(BaseSettings):
    """
    Central settings for the Multimodal AI Workspace.
    """

    app_name: str = Field(
        default="Multimodal AI Workspace",
        alias="APP_NAME",
    )

    debug: bool = Field(
        default=True,
        alias="DEBUG",
    )

    openai_api_key: str | None = Field(
        default=None,
        alias="OPENAI_API_KEY",
    )

    openai_vision_model: str = Field(
        default="gpt-4o-mini",
        alias="OPENAI_VISION_MODEL",
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


def validate_openai_settings(settings: Settings | None = None) -> None:
    """
    Validate OpenAI settings for integrated model-based demos.
    """
    settings = settings or get_settings()

    if not settings.openai_api_key:
        raise ValueError(
            "OPENAI_API_KEY is required for integrated OpenAI demos."
        )


def ensure_directories() -> None:
    """
    Create required project directories if they do not exist.
    """
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    DIAGRAMS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    INTEGRATED_UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    INTEGRATED_IMAGES_DIR.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    settings = get_settings()
    ensure_directories()

    print("Project root:", PROJECT_ROOT)
    print("Portfolio root:", PORTFOLIO_ROOT)
    print("Screenshots dir:", SCREENSHOTS_DIR)
    print("Diagrams dir:", DIAGRAMS_DIR)
    print("Outputs dir:", OUTPUTS_DIR)
    print("Logs dir:", LOGS_DIR)
    print("Integrated uploads dir:", INTEGRATED_UPLOADS_DIR)
    print("Integrated images dir:", INTEGRATED_IMAGES_DIR)
    print("App name:", settings.app_name)
    print("Vision model:", settings.openai_vision_model)
    print("OpenAI key configured:", bool(settings.openai_api_key))