from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_DIR = PROJECT_ROOT / "workspace"
NOTES_DIR = WORKSPACE_DIR / "notes"
TASKS_DIR = WORKSPACE_DIR / "tasks"
DOCUMENTS_DIR = WORKSPACE_DIR / "documents"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
LOGS_DIR = PROJECT_ROOT / "logs"


class Settings(BaseSettings):
    """
    Central settings for the MCP Workspace Assistant.
    """

    app_name: str = Field(
        default="MCP Workspace Assistant",
        alias="APP_NAME",
    )
    debug: bool = Field(default=True, alias="DEBUG")

    openai_api_key: str | None = Field(
        default=None,
        alias="OPENAI_API_KEY",
    )

    primary_llm_provider: Literal["openai"] = Field(
        default="openai",
        alias="PRIMARY_LLM_PROVIDER",
    )

    openai_model: str = Field(
        default="gpt-4o-mini",
        alias="OPENAI_MODEL",
    )

    max_file_read_chars: int = Field(
        default=8000,
        alias="MAX_FILE_READ_CHARS",
    )

    max_search_results: int = Field(
        default=10,
        alias="MAX_SEARCH_RESULTS",
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
    Validate required settings before running the assistant.
    """
    settings = settings or get_settings()

    if settings.primary_llm_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is required when "
                "PRIMARY_LLM_PROVIDER=openai"
            )

    if settings.max_file_read_chars <= 0:
        raise ValueError("MAX_FILE_READ_CHARS must be greater than 0.")

    if settings.max_search_results <= 0:
        raise ValueError("MAX_SEARCH_RESULTS must be greater than 0.")


def ensure_directories() -> None:
    """
    Create required project directories if they do not exist.
    """
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    settings = get_settings()
    ensure_directories()

    print("Project root:", PROJECT_ROOT)
    print("Workspace dir:", WORKSPACE_DIR)
    print("Notes dir:", NOTES_DIR)
    print("Tasks dir:", TASKS_DIR)
    print("Documents dir:", DOCUMENTS_DIR)
    print("Outputs dir:", OUTPUTS_DIR)
    print("Logs dir:", LOGS_DIR)
    print("App name:", settings.app_name)
    print("LLM provider:", settings.primary_llm_provider)
    print("OpenAI model:", settings.openai_model)
    print("Max file read chars:", settings.max_file_read_chars)
    print("Max search results:", settings.max_search_results)