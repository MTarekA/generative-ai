from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
UPLOADED_AUDIO_DIR = DATA_DIR / "uploaded_audio"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
LOGS_DIR = PROJECT_ROOT / "logs"


class Settings(BaseSettings):
    """
    Central settings for the AI Voice Meeting Assistant.
    """

    app_name: str = Field(
        default="AI Voice Meeting Assistant",
        alias="APP_NAME",
    )
    debug: bool = Field(default=True, alias="DEBUG")

    openai_api_key: str | None = Field(
        default=None,
        alias="OPENAI_API_KEY",
    )

    transcription_provider: Literal["openai"] = Field(
        default="openai",
        alias="TRANSCRIPTION_PROVIDER",
    )
    summarization_provider: Literal["openai"] = Field(
        default="openai",
        alias="SUMMARIZATION_PROVIDER",
    )

    openai_transcription_model: str = Field(
        default="gpt-4o-mini-transcribe",
        alias="OPENAI_TRANSCRIPTION_MODEL",
    )
    openai_summary_model: str = Field(
        default="gpt-4o-mini",
        alias="OPENAI_SUMMARY_MODEL",
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

    if settings.transcription_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is required when "
                "TRANSCRIPTION_PROVIDER=openai"
            )

    if settings.summarization_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is required when "
                "SUMMARIZATION_PROVIDER=openai"
            )


def ensure_directories() -> None:
    """
    Create required project directories if they do not exist.
    """
    UPLOADED_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    settings = get_settings()
    ensure_directories()

    print("Project root:", PROJECT_ROOT)
    print("Uploaded audio dir:", UPLOADED_AUDIO_DIR)
    print("Outputs dir:", OUTPUTS_DIR)
    print("Logs dir:", LOGS_DIR)
    print("App name:", settings.app_name)
    print("Transcription provider:", settings.transcription_provider)
    print("Summarization provider:", settings.summarization_provider)
    print("Transcription model:", settings.openai_transcription_model)
    print("Summary model:", settings.openai_summary_model)